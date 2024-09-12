from .models import User
from rest_framework import serializers

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'registration_method', 'avatar', 'is_active']
        read_only_fields = ['id', 'registration_method', 'is_active']
        extra_kwargs = {
            'avatar': {'read_only': True}
        }

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user
    
    def save(self, request):
        validated_data = self.validated_data
        user = self.create(validated_data)
        return user