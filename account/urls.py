from django.urls import path

from account.api import UserAPIView, UserTokenAPIView


urlpatterns = [
    path('api/v1/account/user', UserAPIView.as_view()),
    path('api/v1/account/token', UserTokenAPIView.as_view()),

]
