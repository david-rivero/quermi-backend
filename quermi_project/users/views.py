from rest_framework.generics import ListCreateAPIView

from .models import QuermiProfileUser
from .serializers import QuermiProfileSerializer


class ProfileView(ListCreateAPIView):
    queryset = QuermiProfileUser.objects.all()
    serializer_class = QuermiProfileSerializer
