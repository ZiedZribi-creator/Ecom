from rest_framework import serializers
from .models import SocialMedia

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta :
        model = SocialMedia
        fields = ('facebook','instagram','youtube',)
