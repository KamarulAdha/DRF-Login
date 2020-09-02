from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    # email = serializers.CharField(validators=[verify_email], max_length=255)
    email = serializers.CharField(max_length=255)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializers a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'firstname', 'lastname', 'phone_num', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            firstname = validated_data['firstname'],
            lastname = validated_data['lastname'],
            phone_num=validated_data['phone_num'],
            password = validated_data['password']
        )

        return user
