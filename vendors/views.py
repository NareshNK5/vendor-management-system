from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Vendor, PurchaseOrder , HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer , HistoricalPerformanceSerializer
from django.db.models import Avg, Count, F, Q
from datetime import timedelta
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(data)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.update_vendor_metrics(request.data['vendor'])
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.update_vendor_metrics(request.data['vendor'])
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        vendor_id = instance.vendor.id
        response = super().destroy(request, *args, **kwargs)
        self.update_vendor_metrics(vendor_id)
        return response

    def update_vendor_metrics(self, vendor_id):
        vendor = Vendor.objects.get(id=vendor_id)
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        if completed_orders.exists():
            on_time_deliveries = completed_orders.filter(delivery_date__lte=F('delivery_date')).count()
            vendor.on_time_delivery_rate = (on_time_deliveries / completed_orders.count()) * 100

            vendor.quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']

            total_response_time = completed_orders.aggregate(
                avg_response_time=Avg(F('acknowledgment_date') - F('issue_date'))
            )['avg_response_time']
            vendor.average_response_time = total_response_time.total_seconds() / 3600  # convert to hours

            fulfilled_orders = completed_orders.filter(Q(status='completed') & Q(quality_rating__isnull=False)).count()
            vendor.fulfillment_rate = (fulfilled_orders / completed_orders.count()) * 100
        vendor.save()
        HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )

class HistoricalPerformanceViewSet(viewsets.ModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer