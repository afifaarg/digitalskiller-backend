# models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserProfile(User):  
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        EMPLOYER = 'EMPLOYER', _('Employer')
        FREELANCER = 'FREELANCER', _('Freelancer')
    
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.FREELANCER)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_staff
    
    @property
    def is_employer(self):
        return self.role == self.Role.EMPLOYER
    
    @property
    def is_freelancer(self):
        return self.role == self.Role.FREELANCER


class EmployerProfile(models.Model):
    user_profile = models.OneToOneField(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='employer_profile'
    )
    contact_person = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    account_type = models.CharField(max_length=100, blank=True)
    registre_commerce = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    is_foreign = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.user_profile.username}"

class FreelancerProfile(models.Model):
    user_profile = models.OneToOneField(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='freelancer_profile'
    )
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True)
    experience = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    portfolio_url = models.CharField(max_length=500, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_profile.username} - {self.skills}"