from rest_framework import serializers
from django.contrib.auth.models import User
from .models import QuermiProfileUser, ProfileLanguage, ProfileServices


class ProfileLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLanguage
        fields = '__all__'


class ProfileServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileServices
        fields = '__all__'


class QuermiProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    available_time = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    def get_name(self, obj):
        return '{first_name} {last_name}'.format(
            first_name=obj.user.first_name,
            last_name=obj.user.last_name
        )

    def get_username(self, obj):
        return obj.user.username

    def get_available_time(self, obj):
        return '{from_hour} - {to_hour}'.format(
            from_hour=obj.available_hour_from.strftime('%H:%M'),
            to_hour=obj.available_hour_to.strftime('%H:%M')
        )

    def get_rate(self, obj):
        return obj.rate

    class Meta:
        model = QuermiProfileUser
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        email = validated_data['email']
        username = email.split('@')[0]
        user = User.objects.create(username=username, email=email)
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')