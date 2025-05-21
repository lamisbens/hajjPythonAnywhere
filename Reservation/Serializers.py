# newhadj/serializers.py

from rest_framework import serializers
from .models import Reservation, Alerte, Itineraire, Emplacement

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['pelerin', 'hotel', 'date_debut', 'date_fin']



class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = ['resolue', 'pelerin', 'type_alerte', 'description', 'statut', 'latitude', 'longitude', 'date_creation']



class ItineraireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itineraire
        fields = ['pelerin', 'date', 'lieu', 'description']



class EmplacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emplacement
        fields = ['pelerin', 'latitude', 'longitude', 'timestamp']

