from rest_framework import serializers
from .models import Diagnose

class DiagnoseSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    
    class Meta:
        model = Diagnose
        fields = ['id', 'image', 'label', 'confidence', 'detail', 'created_at']
        read_only_fields = ['label', 'confidence', 'detail', 'created_at']
        
    # def get_image(self, obj):
    #     request = self.context.get('request')
    #     if request:
    #         image_url = obj.image.url
    #         return request.build_absolute_uri(f'{image_url}/{str(obj.uuid)}')

    #     return None