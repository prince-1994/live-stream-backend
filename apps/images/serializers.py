from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from imagekit.cachefiles import ImageCacheFile
from collections import OrderedDict
# from apps.images.models import Image, ImageAlbum


class ImageSpecField(Base64ImageField):
    def __init__(self, *args, **kwargs):
        self.specs = kwargs.pop('specs', {})
        self.base = kwargs.pop('base', False)
        super().__init__(*args, **kwargs)

    def to_representation(self, original_image):
        if not original_image:
            return None

        result = OrderedDict()

        for field_name, spec in self.specs.items():
            cached = ImageCacheFile(spec(original_image))
            cached.generate()
            result[field_name] = super().to_representation(cached)
            print(cached)

        if self.base:
            result['base'] = super().to_representation(original_image)

        return result

# class ImageSerializer(serializers.ModelSerializer):
#     base = Base64ImageField()
#     class Meta:
#         model = Image
#         fields = ('id', 'base', 'name', 'default')

# class ImageAlbumSerializer(serializers.ModelSerializer):
#     images = ImageSerializer(many=True)
#     class Meta:
#         model = ImageAlbum
#         fields = ('id', 'path', 'images', 'owner')
#         read_only_fields = ('id', 'path', 'owner')

    # def create(self, validated_data):
    #     request = self.context['request']
    #     user = request.user
    #     images_data = validated_data.pop('images')
    #     print(validated_data)
    #     imageAlbum = ImageAlbum.objects.create(owner=user, **validated_data)
    #     imageAlbum.save()
    #     for image_data in images_data:
    #         image = Image.objects.create(album=imageAlbum, **image_data)
    #         image.save()
    #     return imageAlbum

    # def update(self, instance, validated_data):
    #     request = self.context['request']
    #     user = request.user
    #     query_params_dict = dict(request.query_params)
    #     delete_image_ids = query_params_dict.get('delete_images')
    #     if delete_image_ids:
    #         print(dict(request.query_params))
    #         for delete_image_id in delete_image_ids:
    #             try:
    #                 id = int(delete_image_id)
    #                 image = Image.objects.filter(pk=id).first()
    #                 if image and image.album.owner == user:
    #                     image.delete()
    #             except ValueError as e:
    #                 print(e)
    #     if ('images' in validated_data):
    #         images_data = validated_data.pop('images')
    #         for image_data in images_data:
    #             image = Image.objects.create(album=instance, **image_data)
    #             image.save()
    #     imageAlbum = super(ImageAlbumSerializer, self).update(instance, validated_data)
    #     try:
    #         default_id = int(request.query_params.get('default_image'))
    #         print(default_id)
    #     except Exception:
    #         default_id = None
    #     if default_id:
    #         for image in Image.objects.filter(album=imageAlbum):
    #             print(image.id, default_id, image.id == default_id)
    #             if image.default and image.id != default_id:
    #                 image.default = False
    #                 image.save()
    #             elif (not image.default) and image.id == default_id:
    #                 print(image)
    #                 image.default = True
    #                 image.save()
    #     return imageAlbum