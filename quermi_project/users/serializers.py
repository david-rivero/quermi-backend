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

    def get_name(self, obj):
        return '{first_name} {last_name}'.format(
            first_name=obj.user.first_name,
            last_name=obj.user.last_name
        )

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
        fields = ('id', 'email', 'password',)