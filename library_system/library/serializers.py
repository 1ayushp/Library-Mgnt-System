from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role','rented_books']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
