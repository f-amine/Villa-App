from rest_framework import serializers
from .models import Availability, Reservation, DatePricing

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'



class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class DatePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatePricing
        fields = '__all__'