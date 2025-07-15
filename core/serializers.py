from rest_framework import serializers
from .models import Vehicle, Service, Location  # ✅ make sure you have these models

class PingSerializer(serializers.Serializer):
    message = serializers.CharField()

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
