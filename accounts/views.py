# django imports
from django.contrib.auth import login

# rest_framework imports
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.authtoken.serializers import AuthTokenSerializer

# knox imports
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

# local apps import
from .serializers import UserSerializer, AuthSerializer

from rest_framework.authentication import SessionAuthentication


class CreateUserView(generics.CreateAPIView):
    # Create user API view
    serializer_class = UserSerializer


class LoginView(KnoxLoginView):
    # login view extending KnoxLoginView
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
