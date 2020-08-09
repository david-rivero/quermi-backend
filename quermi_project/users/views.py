from rest_framework.generics import (
    ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView)
from django.contrib.auth.models import User

from .models import QuermiProfileUser, ProfileServices, ProfileLanguage
from .serializers import (
    QuermiProfileSerializer,
    UserSerializer,
    ProfileLanguageSerializer,
    ProfileServicesSerializer
)


class ProfileLanguageView(ListAPIView):
    queryset = ProfileLanguage.objects.all()
    serializer_class = ProfileLanguageSerializer


class ProfileServicesView(ListAPIView):
    queryset = ProfileServices.objects.all()
    serializer_class = ProfileServicesSerializer


class ProfileView(ListCreateAPIView):
    queryset = QuermiProfileUser.objects.all()
    serializer_class = QuermiProfileSerializer


class ProfileDetailView(RetrieveUpdateDestroyAPIView):
    # queryset?
    serializer_class = QuermiProfileUser

    def get_queryset(self):
        id_profile = self.kwargs.get('pk')
        return QuermiProfileUser.objects.filter(pk=id_profile) # Not working

class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
