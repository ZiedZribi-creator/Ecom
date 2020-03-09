from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status,generics
from .models import Order,GuestUserForm
from .serializers import (OrderSerializer,)
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

class OrderViewset(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class= StandardResultsSetPagination

    def get_queryset(self):
        qs = Order.objects.all()
        email = self.request.GET.get('email')
        client_name = self.request.GET.get('client_name')
        status = self.request.GET.get('status')
        phone = self.request.GET.get('phone_number')
        if email or client_name or status or phone :
            if email :
                qs = qs.filter(guestuserform__email__icontains=email)
            if client_name :
                qs = qs.filter(guestuserform__name__icontains=client_name)
            if status != '' :
                qs = qs.filter(status=status)
            if phone :
                print(phone)
                qs = qs.filter(guestuserform__phone__icontains=phone)
            return qs
        return qs
    @action(methods=['put'],detail=True)
    def set_status(self,request,pk):
        order_obj = self.get_object()
        order_status = self.request.data.get('status')
        order_obj.status = order_status
        order_obj.save()
        return Response({'response':'status updated'},status=status.HTTP_200_OK)
    # @action(methods=['put'],detail=False)
    # def custom_creation(self,request,pk=None):
    #     order_obj = self.get_object()
    #     order_obj.attach_shipping_info(shipping_info=request.POST)
    #     return Response({'response':'shipping info attached'},status=status.HTTP_200_OK)
    #
    # @action(methods=['put'],detail=True)
    # def attach_shipping_info(self,request,pk):
    #     order_obj = self.get_object()
    #     order_obj.attach_shipping_info(shipping_info=request.POST)
    #     return Response({'response':'shipping info attached'},status=status.HTTP_200_OK)
    #
    # @action(methods=['put'],detail=True)
    # def set_order_status(self,request,pk):
    #     order_obj = self.get_object()
    #     order_status = request.POST.get('prder_status')
    #     order_obj.status = order_status
    #     order_obj.save()
    #     return Response({'response':'order status updated'},status=status.HTTP_200_OK)
    #
    # @action(methods=['put'],detail=True)
    # def add_event(self,request,pk):
    #     order_obj = self.get_object()
    #     event = request.POST.get('event')
    #     order.add_event(event=event)
    #     return Response({'response':'event added to the order'},status=status.HTTP_200_OK)
