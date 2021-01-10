from rest_framework.serializers import ModelSerializer
from payments.models import (
    PaymentRegister, SubscriptionMode, SubscriptionRegister)


class PaymentRegisterSerializer(ModelSerializer):
    class Meta:
        model = PaymentRegister
        fields = '__all__'


class SubscriptionModeSerializer(ModelSerializer):
    class Meta:
        model = SubscriptionMode
        fields = '__all__'


class SubscriptionRegisterSerializer(ModelSerializer):
    class Meta:
        model = SubscriptionRegister
        fields = '__all__'