from django.contrib import admin
from .models import MovementType, Status, Category, Subcategory, CashFlow

@admin.register(MovementType)
class MovementTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "movement_type")
    list_filter = ("movement_type",)
    search_fields = ("name",)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)

@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    list_display = ("record_date", "status", "movement_type", "category", "subcategory", "amount")
    list_filter = ("record_date", "status", "movement_type", "category", "subcategory")
    search_fields = ("comment",)
    date_hierarchy = "record_date"
