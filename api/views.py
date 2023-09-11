from rest_framework import status
from django.shortcuts import render
from rest_framework import generics
from .models import Store
from .serializers import StoreSerializer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import subprocess


# Create your views here.


class StoreListAPI(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['scrip']


class StoreDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated,]


class MultipleDeleteView(generics.DestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated,]

    def delete(self, request, *args, **kwargs):
        try:
            pk_list = request.data['pk_list']
        except KeyError:
            return Response({'pk_list': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        self.queryset.filter(pk__in=pk_list).delete()

        return Response({"message": "data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ImportCSVView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            subprocess.run(['python', 'manage.py', 'import_csv',
                           'data/data.csv'], check=True, shell=True)
            return Response({"message": "CSV file imported successfully."}, status=status.HTTP_200_OK)
        except subprocess.CalledProcessError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
