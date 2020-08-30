from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView

from services.models import Contract
from services.serializers import ContractReadOnlySerializer
class ContractListView(ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractReadOnlySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        'patient__username',
        'care_person__username',
    ]

