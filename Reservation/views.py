from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Reservation, Alerte, Itineraire, Emplacement, ScannedQRCode, Rituel, RituelSteps
from .Serializers import (
    ReservationSerializer,
    AlerteSerializer,
    ItineraireSerializer,
    EmplacementSerializer,
    ScannedQRCodeSerializer,
    RituelSerializer
)
from rest_framework.response import Response


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]


class AlerteViewSet(viewsets.ModelViewSet):
    serializer_class = AlerteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        print(user.type)

        # If user is a pelerin, show only their medical emergency alerts
        if user.type == 'pelerin':
            return Alerte.objects.filter(
                pelerin=user.pelerin
            ).order_by('-date_creation')

        # If user is a guide, show medical emergency alerts of their assigned pelerins
        elif user.type == 'guide':
            return Alerte.objects.filter(
                pelerin__guide=user,
                type_alerte='urgence'
            ).order_by('-date_creation')

        # For admin, show all medical emergency alerts (or adjust as needed)
        else:
            return Alerte.objects.filter(
                type_alerte='urgence'
            ).order_by('-date_creation')

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


# ----------- Rituals api ------------
class Ritualsinfo(APIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = []

        try:
            rituelact = RituelSteps.objects.get(
                            pelerin=user.pelerin,
                            statut=False
                        ).rituel

            print(rituelact)
        except RituelSteps.DoesNotExist:
            rituelact = 'Completé'



        if(user.pelerin.type_pelerinage == "Omra"):
            rituals = Rituel.objects.filter(type_rituel="omra")
        else:
            rituals  = Rituel.objects.filter(type_rituel="omra")

        done = True
        for elem in rituals:
            if (rituelact == "Completé"):
                data.append({
                    "titre": elem.titre,
                    "description": elem.description,
                    "done": True,
                    "act": False
                })
            else:
                print("coucou")
                if(elem == rituelact):
                    act = True
                    done = False
                else:
                    act = False
                data.append({
                    "titre": elem.titre,
                    "description": elem.description,
                    "done": done,
                    "act": act
                })




        return Response(data)
