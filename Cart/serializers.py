from rest_framework import serializers
from .models import Cart
from Product.serializers import ClientProductSerializer


class CartSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='user.username')
    products = serializers.SerializerMethodField()
    class Meta :
        model = Cart
        fields = ('id','products','total')
    def get_products(self,cart_obj):
        clientproduct_qs = cart_obj.products.all()
        serializer = ClientProductSerializer(clientproduct_qs,many=True)
        return serializer.data
