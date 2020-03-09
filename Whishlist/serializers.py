from rest_framework import serializers
from .models import WhishList

class WhishListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    products = serializers.SerializerMethodField()
    class Meta :
        model = WhishList
        fields = ('id','username','products')
    def get_products(self,wishlist_obj):
        product_qs = wishlist_obj.products.all()
        serializer = ProductSerializer(product_qs,many=True)
        return serializer.data
