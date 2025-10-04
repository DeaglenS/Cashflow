from django import forms
from .models import CashFlow, Subcategory

class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = [
            "record_date",
            "status",
            "movement_type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]
        widgets = {
            "record_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0.01", "class": "form-control"}),
            "comment": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ("record_date", "amount", "comment"):
                field.widget.attrs.update({"class": "form-select"})
        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["subcategory"].queryset = Subcategory.objects.filter(category_id=category_id)
            except (TypeError, ValueError):
                self.fields["subcategory"].queryset = Subcategory.objects.none()
        elif self.instance.pk:
            self.fields["subcategory"].queryset = Subcategory.objects.filter(category=self.instance.category)
        else:
            self.fields["subcategory"].queryset = Subcategory.objects.none()
