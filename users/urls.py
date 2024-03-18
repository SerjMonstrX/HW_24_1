from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UsersListAPIView

app_name =UsersConfig.name


urlpatterns = [
    path('payments/', PaymentsListAPIView.as_view()),
    path('users/', UsersListAPIView.as_view()),
]
