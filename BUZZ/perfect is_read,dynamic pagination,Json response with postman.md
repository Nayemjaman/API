## postman Documentation.

https://documenter.getpostman.com/view/26172906/2s9YJgSzZy


# models

class Notification(models.Model):
    sellerName = models.CharField(max_length=100, null=True, blank=True)
    buyerName = models.CharField(max_length=100, null=True, blank=True)
    mId = models.CharField(max_length=255, null=True, blank=True)
    sellerId = models.IntegerField(null=True, blank=True)
    buyerId = models.IntegerField(null=True, blank=True)
    orderId = models.IntegerField(null=True, blank=True)
    STATUS_CHOICES = (
        ("Placed", "Placed"),
        ("Accepted", "Accepted"),
        ("Cancel", "Cancel"),
        ("Partially_Delivered", "Partially Delivered"),
        ("Returned_Items", "Returned Items"),
        ("Delivered", "Delivered"),
        ("Partially_Paid", "Partially Paid"),
        ("Paid", "Paid"),
        ("Scheduled For Delivery", "Scheduled For Delivery"),
        ("Delivery Failed", "Delivery Failed"),
        ("Spam", "Spam")
    )

    orderStatus = models.CharField(
        max_length=50, choices=STATUS_CHOICES, null=False)
    seller_read = models.BooleanField(default=False)
    buyer_read = models.BooleanField(default=False)
    new = models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)



# views


from rest_framework import generics, status
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.http.response import JsonResponse

# Create your views here.


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 50
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


class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    # def perform_create(self, serializer):
    #     serializer.save(seller_read=False)
    #     serializer.save(buyer_read=False)

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


class NotificationUpdateView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        orderId = self.kwargs.get('orderId')
        instance, created = Notification.objects.get_or_create(orderId=orderId)
        return instance

    def update(self, request, *args, **kwargs):
        instance = self.get_queryset()

        mutable_data = request.data.copy()
        mutable_data['seller_read'] = False  # Set seller_read to False
        mutable_data['buyer_read'] = False  # Set buyer_read to False

        serializer = self.get_serializer(
            instance, data=mutable_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        result = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Notification updated successfully",
            "result": serializer.data
        }


class SellerNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        sellerId = self.kwargs['sellerId']
        queryset = Notification.objects.filter(
            sellerId=sellerId).order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        result = {
            "status": status.HTTP_200_OK,
            "success": True,
            "page": self.paginator.page.number,
            "message": "Notifications for sellerId",
            "results": serializer.data
        }

        return Response(result)


class BuyerNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        buyerId = self.kwargs['buyerId']
        queryset = Notification.objects.filter(buyerId=buyerId).order_by('-id')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        result = {
            "status": status.HTTP_200_OK,
            "success": True,
            "page": self.paginator.page.number,
            "message": "Notifications for BuyerId",
            "results": serializer.data
        }

        return Response(result)


class SellerNotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        sellerId = self.kwargs.get('sellerId')
        notification_id = self.kwargs.get('pk')
        try:
            return Notification.objects.filter(id=notification_id, sellerId=sellerId)
        except Notification.DoesNotExist:
            raise JsonResponse({"status": status.HTTP_200_OK,
                               "success": True, "message": "ok"})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.seller_read = True
        instance.save()
        serializer = self.serializer_class(instance)

        result = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Notification by SellerId",
            "result": serializer.data
        }
        return Response(result)


class BuyerNotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        buyerId = self.kwargs.get('buyerId')
        notification_id = self.kwargs.get('pk')
        try:
            return Notification.objects.filter(id=notification_id, buyerId=buyerId)
        except Notification.DoesNotExist:
            raise JsonResponse({"status": status.HTTP_200_OK,
                               "success": True, "message": "ok"})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.buyer_read = True
        instance.save()
        serializer = self.serializer_class(instance)

        result = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Notification by SellerId",
            "result": serializer.data
        }
        return Response(result)


class SellerUnreadNotificationCountView(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, sellerId):
        unread_count = Notification.objects.filter(
            sellerId=sellerId, seller_read=False).count()
        return Response({'unread_count': unread_count}, status=status.HTTP_200_OK)


class BuyerUnreadNotificationCountView(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, buyerId):
        unread_count = Notification.objects.filter(
            buyerId=buyerId, buyer_read=False).count()
        return Response({'unread_count': unread_count}, status=status.HTTP_200_OK)

# Urls

from django.urls import path
from .views import (NotificationCreateView, NotificationUpdateView,
                    SellerNotificationListView, BuyerNotificationListView, 
                    SellerNotificationDetailView, BuyerNotificationDetailView, 
                    SellerUnreadNotificationCountView, BuyerUnreadNotificationCountView)

urlpatterns = [
    path('notification/', NotificationCreateView.as_view()),  
    path('notification/update/<int:orderId>/', NotificationUpdateView.as_view()), 


    path('notification/seller/<int:sellerId>/', SellerNotificationListView.as_view()),  
    path('notification/buyer/<int:buyerId>/', BuyerNotificationListView.as_view()),  


    path('notification/seller/<int:sellerId>/<int:pk>/', SellerNotificationDetailView.as_view()),
    path('notification/buyer/<int:buyerId>/<int:pk>/', BuyerNotificationDetailView.as_view()),


    path('notification/seller/unread_count/<int:sellerId>/', SellerUnreadNotificationCountView.as_view()),
    path('notification/buyer/unread_count/<int:buyerId>/', BuyerUnreadNotificationCountView.as_view()),
]



# dynamic pagination.

http://127.0.0.1:8000/notification/77/?page=2&limit=2
