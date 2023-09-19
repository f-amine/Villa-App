from rest_framework import serializers
from .models import Availability, Reservation, DatePricing, Review

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
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
# class InvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields = '__all__'