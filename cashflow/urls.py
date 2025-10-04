from django.urls import path
from . import views

urlpatterns = [
    path("", views.cashflow_list, name="cashflow_list"),
    path("cashflows/create/", views.cashflow_create, name="cashflow_create"),
    path("cashflows/<int:pk>/edit/", views.cashflow_edit, name="cashflow_edit"),
    path("cashflows/<int:pk>/delete/", views.cashflow_delete, name="cashflow_delete"),

    path("ajax/subcategories/", views.subcategories_for_category, name="ajax_subcategories"),
]
