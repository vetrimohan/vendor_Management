from rest_framework import serializers
from .models import Ventor,PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ventor

        fields='__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder

        fields='__all__'
        