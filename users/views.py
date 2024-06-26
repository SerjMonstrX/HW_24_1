import stripe
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserProfileSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]


class UsersListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserProfileSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]  # Требует аутентификации

    def perform_create(self, serializer):
        user = self.request.user

        # Проверка наличия курса или урока
        course = serializer.validated_data.get('course')
        lesson = serializer.validated_data.get('lesson')
        if not course and not lesson:
            raise ValueError("Должен быть указан либо курс, либо урок")

        with transaction.atomic():
            # Создание платежа
            payment = serializer.save(user=user)
            try:
                if course:
                    name = f"Оплата курса {course.name}"
                    description = course.description
                else:
                    name = f"Оплата урока {lesson.name}"
                    description = lesson.description

                product = create_stripe_product(name=name, description=description)
                price = create_stripe_price(product['id'], payment.amount)
                success_url = self.request.build_absolute_uri('/payment/success/')
                cancel_url = self.request.build_absolute_uri('/payment/cancel/')
                session_id, payment_link = create_stripe_session(price['id'], success_url, cancel_url)
                payment.session_id = session_id
                payment.link = payment_link
                payment.save()
            except stripe.error.StripeError as e:
                payment.delete()
                raise e
            except Exception as e:
                payment.delete()
                raise e


class PaymentStatusAPIView(APIView):
    def get(self, request, session_id):
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return Response({'status': session['payment_status']}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
