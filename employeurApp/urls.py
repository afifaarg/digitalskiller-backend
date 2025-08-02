from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, SigninView, EmployerViewSet

router = DefaultRouter()
router.register(r'employers', EmployerViewSet)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('', include(router.urls)),
]