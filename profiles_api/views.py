# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions
from profiles_api.permissions import UpdateOwnProfile


from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey

from profiles_api.models import ExtraInfo

from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)
# from rest_framework_simplejwt.views import TokenRefreshView


# Create your views here.
class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer
    permission_classes = [HasAPIKey & IsAuthenticated]
    # permission_classes = (HasAPIKey,)
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]
        return Response({'message': 'Hello!', 'an_apiview': an_apiview})


    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            message = f'{email} exists'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    permission_classes = [HasAPIKey & UpdateOwnProfile]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class NewTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    permission_classes = (HasAPIKey,)
    # serializer_class = TokenObtainPairSerializer


class NewTokenRefreshView(TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    permission_classes = (HasAPIKey,)
    # serializer_class = serializers.TokenRefreshSerializer


class ExtraInfoViewSet(UserProfileViewSet):
    permission_classes = [HasAPIKey & IsAuthenticated]
    queryset = ExtraInfo.objects.all()
    serializer_class = serializers.ExtraInfoSerializer
