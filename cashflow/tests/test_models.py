from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from cashflow.models import MovementType, Status, Category, Subcategory, CashFlow

class CashflowModelTests(TestCase):
    def setUp(self):
        self.topup = MovementType.objects.create(name="Пополнение")
        self.expense = MovementType.objects.create(name="Списание")
        self.status = Status.objects.create(name="Бизнес")
        self.cat_marketing = Category.objects.create(name="Маркетинг", movement_type=self.expense)
        self.sub_avito = Subcategory.objects.create(name="Avito", category=self.cat_marketing)

    def test_amount_must_be_positive(self):
        cf = CashFlow(
            record_date="2025-01-01",
            status=self.status,
            movement_type=self.expense,
            category=self.cat_marketing,
            subcategory=self.sub_avito,
            amount=Decimal("-1.00"),
        )
        with self.assertRaises(ValidationError):
            cf.full_clean()

    def test_category_must_match_type(self):
        cf = CashFlow(
            record_date="2025-01-01",
            status=self.status,
            movement_type=self.topup,
            category=self.cat_marketing,  # belongs to expense
            subcategory=self.sub_avito,
            amount=Decimal("100.00"),
        )
        with self.assertRaises(ValidationError):
            cf.full_clean()

    def test_subcategory_must_match_category(self):
        other_cat = Category.objects.create(name="Инфраструктура", movement_type=self.expense)
        cf = CashFlow(
            record_date="2025-01-01",
            status=self.status,
            movement_type=self.expense,
            category=other_cat,
            subcategory=self.sub_avito,  # belongs to marketing
            amount=Decimal("100.00"),
        )
        with self.assertRaises(ValidationError):
            cf.full_clean()

    def test_valid_cashflow_saves(self):
        cf = CashFlow(
            record_date="2025-01-02",
            status=self.status,
            movement_type=self.expense,
            category=self.cat_marketing,
            subcategory=self.sub_avito,
            amount=Decimal("1000.00"),
        )
        cf.full_clean()
        cf.save()
        self.assertEqual(CashFlow.objects.count(), 1)
