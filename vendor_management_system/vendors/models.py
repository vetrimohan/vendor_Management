from django.db import models
from django.utils import timezone

# Create your models here.
class Ventor(models.Model):
    name=models.CharField(max_length=100)
    contact_details=models.TextField()
    address=models.TextField()
    Ventor_code=models.CharField(max_length=10,unique=True)
    on_time_delivery_rate=models.FloatField(default=0)
    quality_rating_average=models.FloatField(default=0)
    average_response_time=models.FloatField(default=0)
    fulfillment_rate=models.FloatField(default=0)
    def update_performance_metrics(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()
        
        # Calculate on-time delivery rate
        on_time_delivery_count = completed_orders.filter(delivery_date__lte=timezone.now()).count()
        self.on_time_delivery_rate = (on_time_delivery_count / total_completed_orders) * 100 if total_completed_orders > 0 else 0
        
        # Calculate quality rating average
        quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        self.quality_rating_avg = sum(quality_ratings) / total_completed_orders if total_completed_orders > 0 else 0
        
        # Calculate average response time
        response_times = completed_orders.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=models.ExpressionWrapper(models.F('acknowledgment_date') - models.F('issue_date'), output_field=models.DurationField())
        ).values_list('response_time', flat=True)
        self.average_response_time = sum(response_times, timezone.timedelta()) / total_completed_orders if total_completed_orders > 0 else 0
        
        # Calculate fulfillment rate
        fulfilled_orders_count = completed_orders.filter(issue_date__isnull=True).count()
        self.fulfillment_rate = (fulfilled_orders_count / total_completed_orders) * 100 if total_completed_orders > 0 else 0
        
        self.save()


class PurchaseOrder(models.Model):
    po_number=models.CharField(max_length=10,unique=True)
    Ventor=models.ForeignKey(Ventor,on_delete=models.CASCADE)
    order_date=models.DateTimeField()
    delivery_date=models.DateTimeField()
    items=models.JSONField()
    quantity=models.IntegerField()
    status=models.CharField(max_length=20)
    quality_rating=models.FloatField(null=True)
    issue_date=models.DateTimeField()
    acknowledgement_date=models.DateTimeField(null=True)
    def acknowledge(self):
        if self.status == 'completed' and self.acknowledgement_date is None:
            self.acknowledgement_date = timezone.now()
            self.save()

    
class HistoricalPerformance(models.Model):
    Ventor=models.ForeignKey(Ventor,on_delete=models.CASCADE)
    date=models.DateTimeField()
    on_time_delivary_rate=models.FloatField()
    quality_rating_avg=models.FloatField()
    avg_response_time=models.FloatField()
    fulfillment_rate = models.FloatField()

    @classmethod
    def calculate_performance_metrics(cls, ventor):
        # Calculate performance metrics based on completed purchase orders for the vendor
        completed_orders = PurchaseOrder.objects.filter(Ventor=ventor, status='completed')

        total_completed_orders = completed_orders.count()
        if total_completed_orders == 0:
            return None  # No completed orders, return None or handle appropriately

        on_time_delivery_count = completed_orders.filter(delivery_date__lte=timezone.now()).count()
        on_time_delivery_rate = (on_time_delivery_count / total_completed_orders) * 100

        quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        quality_rating_avg = sum(quality_ratings) / total_completed_orders

        response_times = completed_orders.exclude(acknowledgement_date__isnull=True).annotate(
            response_time=models.ExpressionWrapper(models.F('acknowledgement_date') - models.F('issue_date'), output_field=models.DurationField())
        ).values_list('response_time', flat=True)

        # Calculate the average response time in seconds
        avg_response_time_seconds = sum(response.total_seconds() for response in response_times) / total_completed_orders

        fulfilled_orders_count = completed_orders.filter(issue_date__isnull=True).count()
        fulfillment_rate = (fulfilled_orders_count / total_completed_orders) * 100

        # Create and save HistoricalPerformance instance
        historical_performance = cls(
            Ventor=ventor,
            date=timezone.now(),
            on_time_delivary_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            avg_response_time=avg_response_time_seconds,  # Assign the calculated value
            fulfillment_rate=fulfillment_rate
        )
        historical_performance.save()
        return historical_performance