from django.urls import path
from .views import HelloBroker

urlpatterns = [
    path("welcome/", HelloBroker.as_view(), name="welcome"),
]
