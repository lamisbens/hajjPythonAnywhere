# newhadj/serializers.py

from rest_framework import serializers
from .models import Reservation, Alerte, Itineraire, Emplacement, ScannedQRCode, Rituel


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['pelerin', 'hotel', 'date_debut', 'date_fin']


class AlerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerte
        fields = ['resolue', 'pelerin', 'type_alerte', 'description', 'statut', 'latitude', 'longitude',
                  'date_creation']


class ItineraireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itineraire
        fields = ['pelerin', 'date', 'lieu', 'description']


class EmplacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emplacement
        fields = ['pelerin', 'latitude', 'longitude', 'timestamp']


class ScannedQRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScannedQRCode
        fields = ['code', 'scanned_at']


class RituelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rituel
        fields = ['id', 'titre', 'description', 'ordre', 'type_rituel', 'date_creation']
