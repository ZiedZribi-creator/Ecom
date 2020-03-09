from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status,generics
from .models import WhishList
from .serializers import WhishListSerializer


class WhishListViewset(ModelViewSet):
    queryset = WhishList.objects.all()
    serializer_class = WhishListSerializer

    @action(methods=['put'],detail=True)
    def add_product(self,request,pk):
        whishlist_obj = self.get_object()
        product_id  = request.POST.get('product_id')
        whishlist_obj.add_product(product_id=product_id)
        return Response({'response':'product added'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def switch_product_to_cart(self,request,pk):
        whishlist_obj = self.get_object()
        client_product_id  = request.POST.get('client_product_id')
        whishlist_obj.switch_product_to_cart(client_product_id=client_product_id)
        return Response({'response':'product qty updated'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def drop_product(self,request,pk):
        whishlist_obj = self.get_object()
        client_product_id  = request.POST.get('client_product_id')
        whishlist_obj.drop_product(client_product_id=client_product_id)
        return Response({'response':'product increased'},status=status.HTTP_200_OK)
