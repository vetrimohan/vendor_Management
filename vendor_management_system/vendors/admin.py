from django.contrib import admin
from .models import HistoricalPerformance,PurchaseOrder,Ventor

# Register your models here.
admin.site.register(Ventor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)