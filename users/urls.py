from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UsersListAPIView, UserCreateAPIView, UserRetrieveAPIView, \
    UserUpdateAPIView, UserDestroyAPIView, PaymentCreateAPIView, PaymentStatusAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('payments/', PaymentsListAPIView.as_view(), name='payment_list'),
    path('user_list/', UsersListAPIView.as_view(), name='user_list'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payment/status/<str:session_id>/', PaymentStatusAPIView.as_view(), name='payment_status'),
]
