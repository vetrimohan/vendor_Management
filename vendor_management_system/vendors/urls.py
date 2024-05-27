from django.urls import path
from .views import VentorListCreate,VentorRetrieveUpdateDestroy,PurchaseOrderListCreate,PurchaseOrderRetrieveUpdateDestroy,calculate_performance_metrics,vendor_performance,acknowledge_purchase_order


urlpatterns = [
    path('vendor/', VentorListCreate.as_view(), name='vendor-list'),
    path('vendor/<int:pk>/', VentorRetrieveUpdateDestroy.as_view(), name='vendor-detail'),
    path('purchase_order/', PurchaseOrderListCreate.as_view(), name='purchase_order'),
    path('purchase_order/<int:pk>/', PurchaseOrderRetrieveUpdateDestroy.as_view(), name='purchase_details'),
    path('calculate-performance/<int:vendor_id>/', calculate_performance_metrics, name='calculate_performance_metrics'),
    path('vendors/<int:vendor_id>/performance',vendor_performance, name='vendor_performance'),
    path('purchase_orders/<int:po_id>/acknowledge',acknowledge_purchase_order, name='acknowledge_purchase_order'),
]