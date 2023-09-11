from django.urls import path
from .views import StoreListAPI, StoreDetailAPI, ImportCSVView, MultipleDeleteView

urlpatterns = [
    path('api/stores/', StoreListAPI.as_view(), name='store-list-api'),
    path('api/stores/<int:pk>/', StoreDetailAPI.as_view(), name='store-detail-api'),
    path('api/import-csv/', ImportCSVView.as_view(), name='import-csv'),
    path('api/bulk-delete/', MultipleDeleteView.as_view(),
         name='your-model-bulk-delete'),
]
