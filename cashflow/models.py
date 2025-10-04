from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        abstract = True

class MovementType(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering = ["name"]
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"
    def __str__(self): return self.name

class Status(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering = ["name"]
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
    def __str__(self): return self.name

class Category(TimeStampedModel):
    name = models.CharField(max_length=150)
    movement_type = models.ForeignKey(
        MovementType, on_delete=models.PROTECT, related_name="categories"
    )
    class Meta:
        ordering = ["name"]
        unique_together = ("name", "movement_type")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    def __str__(self): return f"{self.name} ({self.movement_type})"

class Subcategory(TimeStampedModel):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="subcategories"
    )
    class Meta:
        ordering = ["name"]
        unique_together = ("name", "category")
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
    def __str__(self): return f"{self.name} ({self.category})"

class CashFlow(TimeStampedModel):
    record_date = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="cashflows")
    movement_type = models.ForeignKey(MovementType, on_delete=models.PROTECT, related_name="cashflows")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="cashflows")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name="cashflows")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ["-record_date", "-id"]
        constraints = [
            models.CheckConstraint(check=Q(amount__gt=0), name="amount_positive"),
        ]
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"

    def clean(self):
        if self.category_id and self.movement_type_id:
            if self.category.movement_type_id != self.movement_type_id:
                raise ValidationError({
                    "category": "Категория не относится к выбранному типу.",
                    "movement_type": "Выбранный тип не соответствует категории.",
                })
        if self.subcategory_id and self.category_id:
            if self.subcategory.category_id != self.category_id:
                raise ValidationError({
                    "subcategory": "Подкатегория не принадлежит выбранной категории.",
                    "category": "Категория не соответствует подкатегории.",
                })

    def __str__(self):
        return f"{self.record_date} — {self.amount} ({self.category} / {self.subcategory})"
