import json
import os

from django.shortcuts import render

from rest_framework.generics import (
    ListCreateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
import stripe

from django.http import HttpRequest

from payments.models import (
    PaymentRegister, SubscriptionMode, SubscriptionRegister)
from payments.serializers import (
    PaymentRegisterSerializer,
    SubscriptionModeSerializer,
    SubscriptionRegisterSerializer
)
from users.models import QuermiProfileUser


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


class CustomerSubscriptionListView(ListCreateAPIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = SubscriptionRegisterSerializer
    queryset = SubscriptionRegister.objects.all()

    def get(self, request, *args, **kwargs):
        profile = request.query_params.get('profile') or None
        if profile:
            res = SubscriptionRegister.objects.filter(
                profile__user__username=profile)
            if res.count():
                subscription_id = res.first().sub_payment_id

                subscription = stripe.Subscription.retrieve(subscription_id)

                product_subscription = subscription['items']['data'][0]
                price_id = product_subscription['price']['id']
                subscription_mode_instance = SubscriptionMode.objects.get(
                    subscription_id=price_id)

                return Response({
                    'period_end': subscription['current_period_end'],
                    'period_start': subscription['current_period_start'],
                    'status': subscription['status'],
                    'currency': product_subscription['price']['currency'],
                    'mode': product_subscription['price']['recurring']['interval'],
                    'price': subscription_mode_instance.price,
                    'name': subscription_mode_instance.name,
                    'id': subscription_id,
                    'instance_id': res.first().pk
                })

        return Response({})

    def post(self, request, *args, **kwargs):
        try:
            # Attach the payment method to the customer
            stripe.PaymentMethod.attach(
                request.data['paymentMethodId'],
                customer=request.data['customerId'],
            )
            # Set the default payment method on the customer
            stripe.Customer.modify(
                request.data['customerId'],
                invoice_settings={
                    'default_payment_method': request.data['paymentMethodId'],
                },
            )

            # Create the subscription
            subscription = stripe.Subscription.create(
                customer=request.data['customerId'],
                items=[
                    {
                        'price': request.data['priceId']
                    }
                ],
                expand=['latest_invoice.payment_intent'],
            )

            serializer = self.get_serializer(data={
                'sub_payment_id': subscription.get('id'),
                'profile': request.data['profileId']
            })
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response(
                str(e), status=status.HTTP_400_BAD_REQUEST)


class CustomerSubscriptionDetailView(DestroyAPIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = SubscriptionRegisterSerializer
    queryset = SubscriptionRegister.objects.all()

    def delete(self, request, *args, **kwargs):
        stripe.Subscription.delete(request.data.pop('subscriptionId'))
        return super(CustomerSubscriptionDetailView, self).delete(
            request, *args, **kwargs)


class SubscriptionModeListView(ListCreateAPIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = SubscriptionModeSerializer
    queryset = SubscriptionMode.objects.all()


class PaymentRegisterListView(ListCreateAPIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = PaymentRegisterSerializer
    queryset = PaymentRegister.objects.all()

    def get(self, request, *args, **kwargs):
        profile = request.query_params.get('profile') or None
        instance = self.serializer_class(PaymentRegister.objects.filter(
            profile__user__username=profile), many=True)
        return Response(instance.data)

    def post(self, request, *args, **kwargs):
        profile = QuermiProfileUser.objects.get(
            pk=request.data.get('profile'))
        stripe.PaymentMethod.attach(
            request.data.get('payment_id'),
            customer=profile.customer_payment_id
        )
        return super(
            PaymentRegisterListView, self).post(request, *args, **kwargs)


class PaymentRegisterDetailView(DestroyAPIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = PaymentRegisterSerializer
    queryset = PaymentRegister.objects.all()

    def delete(self, request, *args, **kwargs):
        stripe.PaymentMethod.detach(request.data.pop('paymentId'))
        return super(
            PaymentRegisterDetailView, self).delete(request, *args, **kwargs)
