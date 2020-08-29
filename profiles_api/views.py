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
# from rest_framework.permissions import IsAuthenticated
from multiple_permissions.permissions import IsAuthenticated

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework_api_key.permissions import HasAPIKey

from rest_condition import ConditionalPermission, C, And, Or, Not
# Create your views here.
class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer
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
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.UpdateOwnProfile,)
    permission_classes = [HasAPIKey & UpdateOwnProfile]
    # permission_classes = And(HasAPIKey, UpdateOwnProfile),
    # permission_classes = ((UpdateOwnProfile & HasAPIKey),)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


# class UserLoginApiView(ObtainAuthToken):
#     """Handle creating user authentication tokens"""
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
