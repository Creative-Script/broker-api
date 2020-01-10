from django.urls import path, include

from broker.apps.authentication.views import RegistrationAPIView

urlpatterns = [
  path('users/register/', RegistrationAPIView.as_view(), name='register-user'),
]
