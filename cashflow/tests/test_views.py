from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from cashflow.models import MovementType, Status, Category, Subcategory, CashFlow

class CashflowViewTests(TestCase):
    def setUp(self):
        self.expense = MovementType.objects.create(name="Списание")
        self.status = Status.objects.create(name="Бизнес")
        self.cat = Category.objects.create(name="Маркетинг", movement_type=self.expense)
        self.sub = Subcategory.objects.create(name="Avito", category=self.cat)

    def test_list_page_renders(self):
        resp = self.client.get(reverse('cashflow_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Записи ДДС')

    def test_create_cashflow_valid(self):
        form_data = {
            'record_date': '2025-01-01',
            'status': self.status.id,
            'movement_type': self.expense.id,
            'category': self.cat.id,
            'subcategory': self.sub.id,
            'amount': '123.45',
            'comment': 'ok',
        }
        resp = self.client.post(reverse('cashflow_create'), form_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(CashFlow.objects.count(), 1)

    def test_edit_cashflow(self):
        obj = CashFlow.objects.create(
            record_date='2025-01-01', status=self.status, movement_type=self.expense,
            category=self.cat, subcategory=self.sub, amount=Decimal('10.00')
        )
        resp = self.client.post(reverse('cashflow_edit', args=[obj.id]), {
            'record_date': '2025-01-02',
            'status': self.status.id,
            'movement_type': self.expense.id,
            'category': self.cat.id,
            'subcategory': self.sub.id,
            'amount': '20.00',
            'comment': 'upd',
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        obj.refresh_from_db()
        self.assertEqual(str(obj.amount), '20.00')

    def test_delete_cashflow(self):
        obj = CashFlow.objects.create(
            record_date='2025-01-01', status=self.status, movement_type=self.expense,
            category=self.cat, subcategory=self.sub, amount=Decimal('10.00')
        )
        resp = self.client.post(reverse('cashflow_delete', args=[obj.id]), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(CashFlow.objects.count(), 0)

    def test_ajax_subcategories(self):
        url = reverse('ajax_subcategories') + f'?category_id={self.cat.id}'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {"results": [{"id": self.sub.id, "name": self.sub.name}]})
