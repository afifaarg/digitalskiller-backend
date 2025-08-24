from django.contrib.auth.models import User
from django.db import models


class Employer(User):
    contactPerson = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    accountType = models.CharField(max_length=100, blank=True)
    registreCommerce = models.CharField(max_length=100, blank=True)
    companyName = models.CharField(max_length=255, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    companySize = models.CharField(max_length=50, blank=True)
    
    is_foreign = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
