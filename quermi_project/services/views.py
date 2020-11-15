from django_filters import rest_framework as filters
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView,
    CreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from django.contrib.auth.models import User

from services.models import Contract, Report
from services.serializers import (
    ContractReadOnlySerializer, ContractWriteSerializer, ReportSerializer)
from utils.messaging import DumbMessageModel

class ContractListView(ListAPIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]
    queryset = Contract.objects.all()
    serializer_class = ContractReadOnlySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        'patient__user__username',
        'care_person__user__username',
    ]

class ContractCreateView(CreateAPIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]
    queryset = Contract.objects.all()
    serializer_class = ContractWriteSerializer

class ContractDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]
    serializer_class = ContractWriteSerializer

    def get_queryset(self):
        id_profile = self.kwargs.get('pk') or None
        return Contract.objects.filter(pk=id_profile)

class ReportListCreateView(ListCreateAPIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ChatRoomView(APIView):
    authentication_classes = [JWTTokenUserAuthentication,]
    permission_classes = [IsAuthenticated,]

    def get(self, request, from_profile='', to_profile=''):
        from_user = User.objects.get(username=from_profile)
        to_user = User.objects.get(username=to_profile)
        room_id = DumbMessageModel.init_chat(from_user.pk, to_user.pk)

        return Response({
            'chat_room_id': room_id
        })
