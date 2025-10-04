from rest_framework import routers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db import models
from django.urls import path, include

from .models import MovementType, Status, Category, Subcategory, CashFlow
from .serializers import (
    MovementTypeSerializer,
    StatusSerializer,
    CategorySerializer,
    SubcategorySerializer,
    CashFlowSerializer,
)
from .filters import CashFlowFilter

class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

class MovementTypeViewSet(BaseModelViewSet):
    queryset = MovementType.objects.all()
    serializer_class = MovementTypeSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "id"]

class StatusViewSet(BaseModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "id"]

class CategoryViewSet(BaseModelViewSet):
    queryset = Category.objects.select_related("movement_type").all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"movement_type": ["exact"]}
    search_fields = ["name"]
    ordering_fields = ["name", "id"]

class SubcategoryViewSet(BaseModelViewSet):
    queryset = Subcategory.objects.select_related("category", "category__movement_type").all()
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {"category": ["exact"]}
    search_fields = ["name"]
    ordering_fields = ["name", "id"]

class CashFlowViewSet(BaseModelViewSet):
    queryset = CashFlow.objects.select_related(
        "status", "movement_type", "category", "subcategory"
    ).all()
    serializer_class = CashFlowSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CashFlowFilter
    ordering_fields = ["record_date", "amount", "id"]
    ordering = ["-record_date", "-id"]

    @action(detail=False, methods=["get"])
    def totals(self, request):
        qs = self.filter_queryset(self.get_queryset())
        total = qs.aggregate(sum_amount=models.Sum("amount"))
        return Response({"sum_amount": total["sum_amount"] or 0})

router = routers.DefaultRouter()
router.register(r"movement-types", MovementTypeViewSet)
router.register(r"statuses", StatusViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"subcategories", SubcategoryViewSet)
router.register(r"cashflows", CashFlowViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
