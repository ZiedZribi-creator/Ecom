from rest_framework import serializers
from .models import ClientProfile,AdminProfile





class ClientProfileSerializer(serializers.ModelSerializer) :

    username = serializers.CharField(source='user.username',read_only=True)
    image = serializers.CharField(source='image.url',read_only=True)


    class Meta :
        model  = AdminProfile
        fields = ('id','slug','user','username','image')


class AdminProfileSerializer(serializers.ModelSerializer) :

    username = serializers.CharField(source='user.username',read_only=True)
    image = serializers.CharField(source='image.url',read_only=True)


    class Meta :
        model  = AdminProfile
        fields = ('id','slug','user','username','image')
