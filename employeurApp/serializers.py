from rest_framework import serializers
from .models import Employer
from django.contrib.auth import authenticate

class EmployerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employer
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'contactPerson', 'phone', 'address', 'website',
            'accountType', 'companyName', 'industry', 'companySize',
            'is_foreign'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Employer(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive")
        return user