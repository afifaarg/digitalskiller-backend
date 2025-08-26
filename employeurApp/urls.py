# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, EmployerProfileViewSet, FreelancerProfileViewSet

router = DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'employers', EmployerProfileViewSet)
router.register(r'freelancers', FreelancerProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]