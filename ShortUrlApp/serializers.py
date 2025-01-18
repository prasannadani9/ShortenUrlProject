from rest_framework import serializers
from .models import UrlDataMainModel, AccessLogs

class UrlDataMainModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlDataMainModel
        fields = ['id', 'main_url', 'short_url', 'expiry_time', 'creation_time']

class AccessLogsSerializer(serializers.ModelSerializer):
    short_url = UrlDataMainModelSerializer(read_only=True)  # Nested serializer to show related `UrlDataMainModel`
    class Meta:
        model = AccessLogs
        fields = ['id', 'short_url', 'ip_address', 'timestamp']
