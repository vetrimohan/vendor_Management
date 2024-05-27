from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from django.utils import timezone
from .models import Ventor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer
from django.views.decorators.http import require_GET



class VentorListCreate(generics.ListCreateAPIView):
    queryset = Ventor.objects.all()
    serializer_class = VendorSerializer

class VentorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ventor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListCreate(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

def calculate_performance_metrics(request, vendor_id):
    try:
        vendor_instance = Ventor.objects.get(id=vendor_id)

        # Call the class method to calculate performance metrics for the vendor
        historical_performance = HistoricalPerformance.calculate_performance_metrics(vendor_instance)

        if historical_performance is not None:
            return JsonResponse({'message': 'Performance metrics calculated and saved successfully!'})
        else:
            return JsonResponse({'message': 'No completed orders found for the vendor.'})
    except Ventor.DoesNotExist:
        return JsonResponse({'error': 'Vendor does not exist.'}, status=404)

@require_GET
def acknowledge_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_id)
        purchase_order.acknowledge()
        return JsonResponse({'message': 'Purchase order acknowledged successfully!'})
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'error': 'Purchase order does not exist.'}, status=404)

@require_GET
def vendor_performance(request, vendor_id):
    try:
        vendor = Ventor.objects.get(id=vendor_id)
        historical_performance = HistoricalPerformance.objects.filter(Ventor=vendor).order_by('-date').first()

        if historical_performance:
            performance_data = {
                'on_time_delivery_rate': historical_performance.on_time_delivary_rate,
                'quality_rating_avg': historical_performance.quality_rating_avg,
                'average_response_time': historical_performance.avg_response_time,
                'fulfillment_rate': historical_performance.fulfillment_rate
            }
            return JsonResponse(performance_data)
        else:
            return JsonResponse({'message': 'No historical performance data found for the vendor.'})
    except Ventor.DoesNotExist:
        return JsonResponse({'error': 'Vendor does not exist.'}, status=404)