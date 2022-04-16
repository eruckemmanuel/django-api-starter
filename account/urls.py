from django.urls import path

from account.api import UserAPIView


urlpatterns = [
    path('api/v1/account/user', UserAPIView.as_view())
]
