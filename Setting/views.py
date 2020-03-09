from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status,generics
from .models import SocialMedia
from .serializers import SocialMediaSerializer
# Create your views here.


class SocialMediaViewset(ModelViewSet):
    serializer_class = SocialMediaSerializer
    queryset = SocialMedia.objects.all()

    @action(methods=['get'],detail=False)
    def get_first(self,request,pk=None):
        sm_obj = SocialMedia.objects.first()
        if sm_obj :
            serializer = SocialMediaSerializer(sm_obj,many=False)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({'res':'there is no social media object'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=False)
    def create_or_update(self,request,pk=None):
        sm_obj = SocialMedia.objects.first()
        sm_data = self.request.data
        if sm_obj :
            sm_obj.update(**sm_data)
            sm_obj.save()
        else :
            sm_obj = SocialMedia.objects.create(**sm_data)
        serializer = SocialMediaSerializer(sm_obj,many=False)
        return Response({'response':serializer.data},status=status.HTTP_200_OK)
