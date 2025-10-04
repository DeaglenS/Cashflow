from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator

from .models import CashFlow, Subcategory
from .forms import CashFlowForm

def cashflow_list(request):
    qs = CashFlow.objects.select_related(
        "status", "movement_type", "category", "subcategory"
    ).all()

    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    status_id = request.GET.get("status")
    type_id = request.GET.get("movement_type")
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")

    if date_from:
        qs = qs.filter(record_date__gte=date_from)
    if date_to:
        qs = qs.filter(record_date__lte=date_to)
    if status_id:
        qs = qs.filter(status_id=status_id)
    if type_id:
        qs = qs.filter(movement_type_id=type_id)
    if category_id:
        qs = qs.filter(category_id=category_id)
    if subcategory_id:
        qs = qs.filter(subcategory_id=subcategory_id)

    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "cashflow_list.html", {"page_obj": page_obj, "params": request.GET})

def cashflow_create(request):
    if request.method == "POST":
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись создана")
            return redirect("cashflow_list")
    else:
        form = CashFlowForm()
    return render(request, "cashflow_form.html", {"form": form, "title": "Создание записи"})

def cashflow_edit(request, pk):
    obj = get_object_or_404(CashFlow, pk=pk)
    if request.method == "POST":
        form = CashFlowForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Изменения сохранены")
            return redirect("cashflow_list")
    else:
        form = CashFlowForm(instance=obj)
    return render(request, "cashflow_form.html", {"form": form, "title": "Редактирование записи"})

def cashflow_delete(request, pk):
    obj = get_object_or_404(CashFlow, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Запись удалена")
        return redirect("cashflow_list")
    return render(request, "cashflow_form.html", {"form": None, "title": "Удалить запись?"})

# Ajax: подкатегории для выбранной категории
def subcategories_for_category(request):
    category_id = request.GET.get("category_id")
    data = []
    if category_id:
        data = list(Subcategory.objects.filter(category_id=category_id).values("id", "name"))
    return JsonResponse({"results": data})
