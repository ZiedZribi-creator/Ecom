from rest_framework import serializers
from .models import GuestUserForm,Order
from Cart.serializers import CartSerializer
from Cart.models import Cart

class GuestUserFormSerializer(serializers.ModelSerializer):

    class Meta :
        model = GuestUserForm
        fields = ('name','email','address','phone',)

# class OrderHistory(serializers.ModelSerializer):
#     class Meta :
#         fields = ('event')

class OrderSerializer(serializers.ModelSerializer):

    cart = serializers.SerializerMethodField(read_only=True)
    guest_user_form = serializers.SerializerMethodField(read_only=True)
    guestuserform = serializers.JSONField(write_only=True)
    cart_id = serializers.IntegerField(write_only=True)
    created_on = serializers.DateTimeField(format="%H:%M:%S / %d-%m-%Y",read_only=True)

    class Meta :
        model = Order
        fields = ('id','cart','created_on','guest_user_form','status','cart_id','guestuserform','cart_id')


    def create(self,validated_data):
        print(dict(validated_data))
        cart_id = validated_data.get('cart_id')
        guest_user_form_data = validated_data.get('guestuserform')
        print(guest_user_form_data)
        guest_user_form_obj = GuestUserForm.objects.create(**guest_user_form_data)
        cart_obj = Cart.objects.get(id=cart_id)
        order_obj = Order.objects.create(cart=cart_obj,guestuserform=guest_user_form_obj)
        return order_obj

    def get_cart(self,order_obj):
        cart_obj   = order_obj.cart
        serializer = CartSerializer(cart_obj,many=False)
        return serializer.data

    def get_guest_user_form(self,order_obj):
        guest_user_form_obj = order_obj.guestuserform
        serializer = GuestUserFormSerializer(guest_user_form_obj,many=False)
        return serializer.data

    # def get_history(self,order_obj):
    #     history_qs = order_obj.history.all()
    #     serializer = HistorySerializer(history_qs,many=True)
    #     return serializer.data
