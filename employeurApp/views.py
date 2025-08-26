# views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import UserProfile, EmployerProfile, FreelancerProfile
from .serializers import (
    UserProfileSerializer, 
    EmployerProfileSerializer, 
    FreelancerProfileSerializer,
    EmployerRegistrationSerializer,
    FreelancerRegistrationSerializer
)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(id=self.request.user.id)


class EmployerProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = EmployerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    data = serializer.validated_data
                    
                    # Create UserProfile
                    user_profile = UserProfile.objects.create_user(
                        username=data['username'],
                        email=data['email'],
                        password=data['password'],
                        first_name=data.get('first_name', ''),
                        last_name=data.get('last_name', ''),
                        role=UserProfile.Role.EMPLOYER,  # Force employer role
                        phone=data.get('phone', '')
                    )
                    
                    # Create employer profile
                    EmployerProfile.objects.create(
                        user_profile=user_profile,
                        company_name=data.get('company_name', ''),
                        contact_person=data.get('contact_person', ''),
                        address=data.get('address', ''),
                        website=data.get('website', ''),
                        industry=data.get('industry', '')
                    )
                    

                    return Response({
                        'message': 'Employer registered successfully',
                        'user_id': user_profile.id,
                        'username': user_profile.username
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FreelancerProfileViewSet(viewsets.ModelViewSet):
    queryset = FreelancerProfile.objects.all()
    serializer_class = FreelancerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = FreelancerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    data = serializer.validated_data
                    
                    # Create UserProfile
                    user_profile = UserProfile.objects.create_user(
                        username=data['username'],
                        email=data['email'],
                        password=data['password'],
                        first_name=data.get('first_name', ''),
                        last_name=data.get('last_name', ''),
                        role=UserProfile.Role.FREELANCER,  # Force freelancer role
                        phone=data.get('phone', '')
                    )
                    
                    # Create freelancer profile
                    FreelancerProfile.objects.create(
                        user_profile=user_profile,
                        skills=data.get('skills', ''),
                        experience=data.get('experience', 0),
                        hourly_rate=data.get('hourly_rate'),
                        bio=data.get('bio', ''),
                        portfolio_url=data.get('portfolio_url', '')
                    )
                    
                    # Optional: Auto-login
                    if request.user.is_anonymous:
                        login(request, user_profile)
                    
                    return Response({
                        'message': 'Freelancer registered successfully',
                        'user_id': user_profile.id,
                        'username': user_profile.username
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)