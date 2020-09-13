from rest_framework import serializers
from services.models import Contract, Report
from users.serializers import QuermiProfileSerializer
from users.models import QuermiProfileUser

class ContractReadOnlySerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    care_person = serializers.SerializerMethodField()

    def get_patient(self, obj):
        q = QuermiProfileUser.objects.get(user=obj.patient.user)
        return QuermiProfileSerializer(q).data

    def get_care_person(self, obj):
        q = QuermiProfileUser.objects.get(user=obj.care_person.user)
        return QuermiProfileSerializer(q).data

    class Meta:
        model = Contract
        fields = [
            'start_date',
            'end_date',
            'status',
            'patient',
            'care_person'
        ]


class ContractWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'