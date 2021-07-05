# from apps.images.models import ImageAlbum
# from apps.images.serializers import ImageAlbumSerializer, ImageSerializer
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import viewsets

# class ImageAlbumViewset(viewsets.ModelViewSet):
#     serializer_class = ImageAlbumSerializer
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         return ImageAlbum.objects.filter(owner=self.request.user)
