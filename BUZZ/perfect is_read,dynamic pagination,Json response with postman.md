#models

from django.db import models


class Notification(models.Model):
    sellerId = models.IntegerField(null=True, blank=True)
    buyerId = models.IntegerField(null=True, blank=True)
    orderId = models.IntegerField(null=True, blank=True)
    STATUS_CHOICES = [
        ('PL', 'Placed'),
        ('AC', 'Accept'),
        ('PP', 'Pick and Pack'),
        ('SD', 'Schedule For Delivery'),
        ('DF', 'Delivery Failed'),
        ('PD', 'Partially Delivered'),
        ('DL', 'Delivered'),
        ('RP', 'Return Product'),
        ('PF', 'Payment Failed'),
        ('PPD', 'Partially Paid'),
        ('PA', 'Paid'),
        ('RF', 'Refunded'),
        ('CN', 'Cancel'),
    ]

    orderStatus = models.CharField(max_length=225,
                                   choices=STATUS_CHOICES,
                                   default='PL'
                                   )
    orderItem = models.JSONField(default=list)
    is_read = models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


#views


from rest_framework import generics, status
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# Create your views here.


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_page_size(self, request):
        """
        Return the page size.
        """
        if self.page_size_query_param:
            try:
                page_size = int(request.query_params.get(
                    self.page_size_query_param, self.page_size))
                if page_size < 1:
                    raise ValueError
                return page_size
            except (TypeError, ValueError):
                pass

        return self.page_size


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        buyerId = self.kwargs['buyerId']
        queryset = Notification.objects.filter(buyerId=buyerId)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        result = {
            "status": status.HTTP_200_OK,
            "success": True,
            "page": self.paginator.page.number,
            "message": "Notifications by BuyerId",
            "results": serializer.data
        }

        return Response(result)


class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def perform_create(self, serializer):
        serializer.save(is_read=False)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        result = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Notification created successfully!",
            "results": serializer.data
        }

        return Response(result)


class NotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.filter(id=self.kwargs['pk'])
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True
        instance.save()
        serializer = self.get_serializer(instance)

        result = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Notification by Id",
            "result": serializer.data
        }
        return Response(result)


urlpatterns = [
    path('notification/', NotificationCreateView.as_view(),
         name='notification-create'),
    path('notification/<int:buyerId>/', NotificationListView.as_view(),
         name='notification-list'),
    path('notificationdetail/<int:pk>/', NotificationDetailView.as_view(),
         name='notification-detail'),

]

#dynamic pagination.
http://127.0.0.1:8000/notification/77/?page=2&limit=2
