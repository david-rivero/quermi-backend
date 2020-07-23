from rest_framework import serializers
from .models import QuermiProfileUser


class QuermiProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuermiProfileUser
        fields = '__all__'