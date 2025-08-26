# serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, EmployerProfile, FreelancerProfile

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'password', 
                 'first_name', 'last_name', 'role', 'phone', 'avatar')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True}
        }

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserProfile(**validated_data)
        user.set_password(password)
        user.save()
        return user

class EmployerProfileSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = EmployerProfile
        fields = '__all__'
        read_only_fields = ('user_profile', 'is_verified', 'created_at', 'updated_at')

class FreelancerProfileSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = FreelancerProfile
        fields = '__all__'
        read_only_fields = ('user_profile', 'created_at', 'updated_at')

# Registration serializers
class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'password', 
                 'first_name', 'last_name', 'role', 'phone', 'avatar')
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'required': True}
        }

    def validate(self, attrs):
        return attrs

# Flat registration serializers (no nested user field)
class EmployerRegistrationSerializer(serializers.Serializer):
    # User fields
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    
    # Employer fields
    company_name = serializers.CharField(required=False, allow_blank=True)
    contact_person = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    website = serializers.CharField(required=False, allow_blank=True)
    industry = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
       
        if UserProfile.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        
        if UserProfile.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        
        return attrs

class FreelancerRegistrationSerializer(serializers.Serializer):
    # User fields
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, validators=[validate_password])
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    
    # Freelancer fields
    skills = serializers.CharField(required=False, allow_blank=True)
    experience = serializers.IntegerField(required=False, min_value=0)
    hourly_rate = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    bio = serializers.CharField(required=False, allow_blank=True)
    portfolio_url = serializers.URLField(required=False, allow_blank=True)

    def validate(self, attrs):
        if  UserProfile.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        
        if  UserProfile.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        
        return attrs