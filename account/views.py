from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets,status,generics
from .models import User,AdminProfile,ClientProfile
from .serializers import AdminProfileSerializer,ClientProfileSerializer
from .UserSerializer import UserSerializer
from .permissions import IsOwnerAndAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permissons_classes = (IsOwnerAndAuthenticated,)


    @action(methods=['GET'],detail=False)
    def email_exist(self,request):
        email  = request.data.get('email')
        qs = User.objects.filter(email=email)
        if qs :
            return Response({'exist':True},status=status.HTTP_200_OK)
        else :
            return Response({'exist':False},status=status.HTTP_200_OK)

class AdminProfileViewSet(viewsets.ModelViewSet):
    serializer_class = AdminProfileSerializer
    queryset = AdminProfile.objects.all()
    lookup_field = 'slug'
    permissons_classes = (IsOwnerAndAuthenticated,)

    @action(methods=['GET'],detail=False)
    def get_info(self,request):
        profile_obj = self.request.user.adminprofile
        serializer  = AdminProfileSerializer(profile_obj,many=False)
        return Response({'response':serializer.data},status=status.HTTP_200_OK)

    @action(methods=['PUT'],detail=True)
    def set_password(self,request,slug):
        profile_admin_obj = self.get_object()
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        print(old_password)
        print(new_password)
        if old_password and new_password :

            user_obj = profile_admin_obj.user
            if user_obj.check_password(old_password):
                user_obj.set_password(new_password)
                user_obj.save()
                return Response({'response':'password updated'},status=status.HTTP_200_OK)
            else :
                return Response({'response':'invalid password'},status=status.HTTP_200_OK)
        return Response({'response':'you miss a field'},status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['PUT'],detail=True)
    def reset_name(self,request,slug):
        profile_obj = self.get_object()
        username = self.request.data.get('username')
        if username :
            user_obj = profile_obj.user
            user_obj.username = username
            user_obj.save()
            return Response({'response':'username updated'},status=status.HTTP_200_OK)
        else :
            return Response({'response':'no username sended'},status=status.HTTP_400_BAD_REQUEST)



    @action(methods=['PUT'],detail=True)
    def reset_image(self,request,slug):
        profile_obj = self.get_object()
        image = self.request.data.get('image')
        if image :
            profile_obj.image = image
            profile_obj.save()
            return Response({'response':'image updated'},status=status.HTTP_200_OK)
        else :
            return Response({'response':'no image sended'},status=status.HTTP_400_BAD_REQUEST)

class ClientProfileViewSet(viewsets.ModelViewSet):
    serializer_class =ClientProfileSerializer
    queryset =ClientProfile.objects.all()
    lookup_field = 'slug'
    permissons_classes = (IsOwnerAndAuthenticated,)


    @action(methods=['PUT'],detail=True)
    def reset_name(self,request,slug):
        profile_obj = self.get_object()
        username = self.request.data.get('username')
        if username :
            user_obj = profile_obj.user
            user_obj.username = username
            user_obj.save()
            return Response({'response':'username updated'},status=status.HTTP_200_OK)
        else :
            return Response({'response':'no username sended'},status=status.HTTP_400_BAD_REQUEST)



    @action(methods=['PUT'],detail=True)
    def reset_image(self,request,slug):
        profile_obj = self.get_object()
        image = self.request.data.get('image')
        if image :
            profile_obj.image = image
            profile_obj.save()
            return Response({'response':'image updated'},status=status.HTTP_200_OK)
        else :
            return Response({'response':'no image sended'},status=status.HTTP_400_BAD_REQUEST)

# class SimpleProfileRetrieveView(generics.RetrieveAPIView):
#     serializer_class = SimpleDoctorProfileSerializer
#     queryset = DoctorProfile.objects.all()
#     lookup_field = 'slug'
