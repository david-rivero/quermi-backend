from django_filters import rest_framework as filters
from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, CreateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User

from services.models import Contract, Report
from services.serializers import (
    ContractReadOnlySerializer, ContractWriteSerializer, ReportSerializer)

from services.models import Contract
from services.serializers import ContractReadOnlySerializer
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

