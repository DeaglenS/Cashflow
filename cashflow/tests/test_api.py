from django.test import TestCase
from rest_framework.test import APIClient
from decimal import Decimal
from cashflow.models import MovementType, Status, Category, Subcategory, CashFlow

class CashflowAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.topup = MovementType.objects.create(name="Пополнение")
        self.expense = MovementType.objects.create(name="Списание")
        self.status_business = Status.objects.create(name="Бизнес")
        self.cat_marketing = Category.objects.create(name="Маркетинг", movement_type=self.expense)
        self.cat_infra = Category.objects.create(name="Инфраструктура", movement_type=self.expense)
        self.sub_avito = Subcategory.objects.create(name="Avito", category=self.cat_marketing)
        self.sub_vps = Subcategory.objects.create(name="VPS", category=self.cat_infra)
        CashFlow.objects.create(record_date="2025-01-01", status=self.status_business,
                                movement_type=self.expense, category=self.cat_marketing,
                                subcategory=self.sub_avito, amount=Decimal("100.00"))
        CashFlow.objects.create(record_date="2025-01-10", status=self.status_business,
                                movement_type=self.expense, category=self.cat_infra,
                                subcategory=self.sub_vps, amount=Decimal("50.00"))

    def _items(self, res):
        return res.data if isinstance(res.data, list) else res.data.get('results', res.data)

    def test_list_movement_types(self):
        res = self.client.get('/api/movement-types/')
        self.assertEqual(res.status_code, 200)
        items = self._items(res)
        self.assertGreaterEqual(len(items), 2)

    def test_categories_filter_by_movement_type(self):
        res = self.client.get(f'/api/categories/?movement_type={self.expense.id}')
        self.assertEqual(res.status_code, 200)
        items = self._items(res)
        self.assertTrue(all(item['movement_type']['id'] == self.expense.id for item in items))

    def test_subcategories_filter_by_category(self):
        res = self.client.get(f'/api/subcategories/?category={self.cat_marketing.id}')
        self.assertEqual(res.status_code, 200)
        items = self._items(res)
        self.assertTrue(all(item['category']['id'] == self.cat_marketing.id for item in items))

    def test_cashflows_filter_and_pagination(self):
        res = self.client.get('/api/cashflows/?date_from=2025-01-01&date_to=2025-01-31')
        self.assertEqual(res.status_code, 200)
        # paginated
        self.assertEqual(res.data['count'], 2)

    def test_cashflows_totals(self):
        res = self.client.get('/api/cashflows/totals/?date_from=2025-01-01&date_to=2025-01-31')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Decimal(str(res.data['sum_amount'])), Decimal('150.00'))

    def test_create_cashflow_validation(self):
        payload = {
            "record_date": "2025-02-01",
            "status": self.status_business.id,
            "movement_type": self.topup.id,  # mismatch with category
            "category": self.cat_marketing.id,
            "subcategory": self.sub_avito.id,
            "amount": "100.00",
            "comment": "test"
        }
        res = self.client.post('/api/cashflows/', payload, format='json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('Категория не относится к выбранному типу', str(res.data))
