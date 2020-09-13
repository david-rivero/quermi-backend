from django_filters import rest_framework as filters
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, CreateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User

from services.models import Contract, Report
from services.serializers import (
    ContractReadOnlySerializer, ContractWriteSerializer, ReportSerializer)
from utils.messaging import DumbMessageModel

class ContractListView(ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractReadOnlySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        'patient__user__username',
        'care_person__user__username',
    ]


class ContractCreateView(CreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractWriteSerializer


class ReportListCreateView(ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ChatRoomView(APIView):
    def get(self, request, from_profile='', to_profile=''):
        from_user = User.objects.get(username=from_profile)
        to_user = User.objects.get(username=to_profile)
        room_id = DumbMessageModel.init_chat(from_user.pk, to_user.pk)

        return Response({
            'chat_room_id': room_id
        })
