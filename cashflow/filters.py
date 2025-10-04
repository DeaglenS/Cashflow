import django_filters as df
from .models import CashFlow

class CashFlowFilter(df.FilterSet):
    date_from = df.DateFilter(field_name="record_date", lookup_expr="gte")
    date_to   = df.DateFilter(field_name="record_date", lookup_expr="lte")

    class Meta:
        model = CashFlow
        fields = {
            "status": ["exact"],
            "movement_type": ["exact"],
            "category": ["exact"],
            "subcategory": ["exact"],
        }
