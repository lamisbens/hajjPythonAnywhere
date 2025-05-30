from rest_framework import viewsets
from .models import Reservation, Alerte, Itineraire, Emplacement, ScannedQRCode, Rituel
from .Serializers import (
    ReservationSerializer,
    AlerteSerializer,
    ItineraireSerializer,
    EmplacementSerializer,
    ScannedQRCodeSerializer,
    RituelSerializer
)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class AlerteViewSet(viewsets.ModelViewSet):
    queryset = Alerte.objects.all()
    serializer_class = AlerteSerializer

class ItineraireViewSet(viewsets.ModelViewSet):
    queryset = Itineraire.objects.all()
    serializer_class = ItineraireSerializer

class EmplacementViewSet(viewsets.ModelViewSet):
    queryset = Emplacement.objects.all()
    serializer_class = EmplacementSerializer

class ScannedQRCodeViewSet(viewsets.ModelViewSet):
    queryset = ScannedQRCode.objects.all()
    serializer_class = ScannedQRCodeSerializer

class RituelViewSet(viewsets.ModelViewSet):
    queryset = Rituel.objects.all()
    serializer_class = RituelSerializer
