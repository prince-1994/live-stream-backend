from apps.profiles.models import Address
from apps.profiles.serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

class AddressViewset(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
        