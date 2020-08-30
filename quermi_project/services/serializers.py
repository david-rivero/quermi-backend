from rest_framework import serializers
from services.models import Contract
from users.serializers import QuermiProfileSerializer
from users.models import QuermiProfileUser

class ContractReadOnlySerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    care_person = serializers.SerializerMethodField()

    def get_patient(self, obj):
        q = QuermiProfileUser.objects.get(user=obj.patient)
        return QuermiProfileSerializer(q).data

    def get_care_person(self, obj):
        q = QuermiProfileUser.objects.get(user=obj.care_person)
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