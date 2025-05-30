from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]

class AlerteViewSet(viewsets.ModelViewSet):
    queryset = Alerte.objects.all()
    serializer_class = AlerteSerializer
    permission_classes = [IsAuthenticated]

class ItineraireViewSet(viewsets.ModelViewSet):
    queryset = Itineraire.objects.all()
    serializer_class = ItineraireSerializer
    permission_classes = [IsAuthenticated]

class EmplacementViewSet(viewsets.ModelViewSet):
    queryset = Emplacement.objects.all()
    serializer_class = EmplacementSerializer
    permission_classes = [IsAuthenticated]

class ScannedQRCodeViewSet(viewsets.ModelViewSet):
    queryset = ScannedQRCode.objects.all()
    serializer_class = ScannedQRCodeSerializer
    permission_classes = [IsAuthenticated]

class RituelViewSet(viewsets.ModelViewSet):
    queryset = Rituel.objects.all()
    serializer_class = RituelSerializer
    permission_classes = [IsAuthenticated]
