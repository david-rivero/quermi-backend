import base64
import os
import random

from django_filters import rest_framework as filters
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import (
    ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView,
    GenericAPIView)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .models import QuermiProfileUser, ProfileServices, ProfileLanguage
from .serializers import (
    QuermiProfileSerializer,
    UserSerializer,
    ProfileLanguageSerializer,
    ProfileServicesSerializer
)
from utils.file_operations import upload_file

TMP_DOC_ID_PHOTO_PATH = '/tmp/doc_id.jpg'
TMP_PROFILE_PHOTO_PATH = '/tmp/profile_ph.jpg'
CREATED_STATUS_CODE = 201
MAX_NUM_LIM = 1000000000


class TokenPairByEmailUser(TokenObtainPairView):
    def get_serializer(self, *args, **kwargs):
        if kwargs.get('data') and kwargs['data'].get('email'):
            email = kwargs['data']['email'] or ''
            user = User.objects.filter(email=email)
            if user.count():
                kwargs['data']['username'] = user.first().username
        return super().get_serializer(*args, **kwargs)


class ProfileLanguageView(ListAPIView):
    queryset = ProfileLanguage.objects.all()
    serializer_class = ProfileLanguageSerializer


class ProfileServicesView(ListAPIView):
    queryset = ProfileServices.objects.all()
    serializer_class = ProfileServicesSerializer


class ProfileView(ListCreateAPIView):
    queryset = QuermiProfileUser.objects.all()
    serializer_class = QuermiProfileSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['user__email', 'role']

    def post(self, request, *args, **kwargs):
        id_doc_b64 = request.data.pop('id_doc_photo')
        profile_photo_b64 = request.data.pop('profile_photo')

        with open(TMP_DOC_ID_PHOTO_PATH,'wb') as fx:
            fx.write(base64.b64decode(id_doc_b64))
            
        with open(TMP_PROFILE_PHOTO_PATH,'wb') as fy:
            fy.write(base64.b64decode(profile_photo_b64))

        response_create = self.create(request, *args, **kwargs)

        if response_create.status_code == CREATED_STATUS_CODE:
            profile_id = response_create.data.get('id')
            profile_user = QuermiProfileUser.objects.get(
                pk=profile_id)
            # first_name, last_name = response_create.data.name.split(' ')
            random_id = random.randint(1, MAX_NUM_LIM)
            id_ph_name = '{}_{}_id_photo'.format(random_id, profile_id)
            profile_ph_name = '{}_{}_profile_photo'.format(
                random_id, profile_id)

            id_ph_ref = upload_file(
                open(TMP_DOC_ID_PHOTO_PATH,'rb'),
                '{}.png'.format(id_ph_name), id_ph_name)
            profile_ref = upload_file(
                open(TMP_PROFILE_PHOTO_PATH,'rb'),
                '{}.png'.format(profile_ph_name), profile_ph_name)

            profile_user.doc_id_photo_url = id_ph_ref
            profile_user.profile_photo_url = profile_ref
            profile_user.save()

            os.remove(TMP_DOC_ID_PHOTO_PATH)
            os.remove(TMP_PROFILE_PHOTO_PATH)

        return response_create

class ProfileDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = QuermiProfileSerializer
    
    def get_queryset(self):
        id_profile = self.kwargs.get('pk') or None
        return QuermiProfileUser.objects.filter(pk=id_profile)

class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
