from apps.profiles.models import Address
from apps.profiles.serializers import EditAddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

class EditAddressViewset(viewsets.ModelViewSet):
    serializer_class = EditAddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(user=user)
        