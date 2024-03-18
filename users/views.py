from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserProfileSerializer


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ['payment_date']

class UsersListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
