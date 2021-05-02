from channels.models import Channel
from rest_framework import serializers
from .models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)

class ProductSerializer(serializers.ModelSerializer):
    # images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'channel', 'price', 'primaryImage', 'sku_id', 'category')
        read_only_fields = ('channel',)

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def create(self, validated_data):
        user = self._user()
        obj = Product.objects.create(owner=user,**validated_data)
        obj.save()
        return obj
    
