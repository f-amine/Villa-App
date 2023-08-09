from rest_framework import serializers
from .models import Villa, Availability, Reservation

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class VillaSerializer(serializers.ModelSerializer):
    availability = AvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Villa
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    villa = VillaSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'