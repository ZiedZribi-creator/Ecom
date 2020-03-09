from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status,generics
from .models import Cart
from .serializers import CartSerializer
from Product.models import ClientProduct,Product

class CartViewset(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    @action(methods=['get'],detail=True)
    def count(self,request,pk):
        cart_obj = self.get_object()
        count = 0
        qs = cart_obj.products.all()
        for client_product in qs :
            count += client_product.qty
        return Response({'cart_count':count},status=status.HTTP_200_OK)
    @action(methods=['put'],detail=False)
    def custom_creation(self,request,pk=None):
        product_slug = self.request.data.get('product_slug')
        product_obj = Product.objects.get(slug=product_slug)
        client_product_obj = ClientProduct.objects.create(product=product_obj)
        cart_obj = Cart.objects.create()
        cart_obj.products.add(client_product_obj)
        cart_obj.save()
        return Response({'cart_id':cart_obj.id},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def add_product(self,request,pk):
        cart_obj = self.get_object()
        product_slug  = request.data.get('product_slug')
        product_obj = Product.objects.get(slug=product_slug)
        qs = ClientProduct.objects.filter(product=product_obj)
        client_product_obj = None
        if qs :
            client_product_obj = qs[0]
            client_product_obj.qty += 1
            client_product_obj.save()
        else :
            client_product_obj = ClientProduct.objects.create(product=product_obj)
        cart_obj.products.add(client_product_obj)
        return Response({'response':'product added'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def set_product_qty(self,request,pk):
        cart_obj = self.get_object()
        client_product_id  = request.data.get('client_product_id')
        qty = self.request.data.get('qty')
        client_product_obj = ClientProduct.objects.get(id=client_product_id)
        client_product_obj.qty = qty
        client_product_obj.save()
        return Response({'response':'product qty updated'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def drop_product(self,request,pk):
        cart_obj = self.get_object()
        client_product_id  = request.data.get('client_product_id')
        client_product_obj = ClientProduct.objects.get(id=client_product_id)
        client_product_obj.delete()
        return Response({'response':'product deleted'},status=status.HTTP_200_OK)
