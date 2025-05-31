import math

from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from googletrans import Translator

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from Session.models import Communication, HeurePriere, AttractionTouristique, Hotel, Pelerin, User, Traduction ,QiblaRequest
from .Serializers import (
    UserSerializer, PelerinSerializer,
    HotelSerializer, AttractionTouristiqueSerializer,
    HeurePriereSerializer, CommunicationSerializer,
    TraductionSerializer, QiblaRequestSerializer, specPelerinSerializer)


# -----------  LoginViewSet -----------
class LoginView(APIView):
    http_method_names = ['post']

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user:
            # User is authenticated
            # Generate or update the token for the user
            token, created = Token.objects.get_or_create(user=user)

            if not created:
                # Token already existed, update the key
                token.delete()
                token = Token.objects.create(user=user)

            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
            })
        else:
            # Invalid credentials
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# ----------- UserInfo ViewSet -----------
class UserInfo(APIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not hasattr(user, 'pelerin'):
            return Response({
                'error': 'User is not a pilgrim',
                'username': user.username,
                'email': user.email
            }, status=200)

        pelerin = user.pelerin
        serializer = specPelerinSerializer(pelerin, context={'request': request})

        data = {
            'username': user.username,
            'email': user.email,
            'pelerin': serializer.data
        }

        return Response(data)

# ----------- User ViewSet -----------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# ----------- Pèlerin ViewSet -----------
class PelerinViewSet(viewsets.ModelViewSet):
    queryset = Pelerin.objects.select_related('user').all()
    serializer_class = PelerinSerializer
    permission_classes = [IsAuthenticated]


# ----------- Hôtel ViewSet -----------
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]


# ----------- Attraction Touristique ViewSet -----------
class AttractionTouristiqueViewSet(viewsets.ModelViewSet):
    queryset = AttractionTouristique.objects.all()
    serializer_class = AttractionTouristiqueSerializer
    permission_classes = [IsAuthenticated]


# ----------- Heure de Prière ViewSet -----------
class HeurePriereViewSet(viewsets.ModelViewSet):
    queryset = HeurePriere.objects.all()
    serializer_class = HeurePriereSerializer
    permission_classes = [IsAuthenticated]


# ----------- Communication ViewSet -----------
class CommunicationViewSet(viewsets.ModelViewSet):
    serializer_class = CommunicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        print(user)

        # If the user is a guide, get all communications with their assigned pelerins
        """if user.type == 'guide':
            pelerin_ids = User.objects.filter(
                pelerin__guide=user
            ).values_list('id', flat=True)
            return Communication.objects.filter(
                Q(sender=user) | Q(receiver=user),
                Q(sender__id__in=pelerin_ids) | Q(receiver__id__in=pelerin_ids)
            ).order_by('timestamp')"""

        # If the user is a pelerin, get communications with their assigned guide
        if user.type == 'pelerin':
            print("here")

            guide = user.pelerin.guide
            liste = Communication.objects.filter(
                    Q(sender=user) |
                    Q(receiver=user)
                ).order_by('timestamp')

            return liste



        # For admin, return all communications (or none, depending on your needs)
        else:
            return Communication.objects.all()

    """def get_queryset(self):
        user = self.request.user
        return Communication.objects.filter(sender=user) | Communication.objects.filter(receiver=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)"""



# ----------- Traduction ViewSet -----------
class TraductionViewSet(viewsets.ModelViewSet):
    queryset = Traduction.objects.all()
    serializer_class = TraductionSerializer

    def create(self, request, *args, **kwargs):
        texte = request.data.get('texte_original')
        langue_source = request.data.get('langue_source', 'auto')
        langue_cible = request.data.get('langue_cible')

        if not texte or not langue_cible:
            return Response({'error': 'texte_original et langue_cible sont requis.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            traducteur = Translator()
            resultat = traducteur.translate(texte, src=langue_source, dest=langue_cible)

            traduction = Traduction.objects.create(
                texte_original=texte,
                texte_traduit=resultat.text,
                langue_source=resultat.src,
                langue_cible=langue_cible
            )
            serializer = self.get_serializer(traduction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# -----------QiblaRequest ViewSet -----------
class QiblaRequestViewSet(viewsets.ModelViewSet):
    queryset = QiblaRequest.objects.all()
    serializer_class = QiblaRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            lat = serializer.validated_data['latitude']
            lon = serializer.validated_data['longitude']

            kaaba_lat = 21.422487
            kaaba_lon = 39.826206

            lat_rad = math.radians(lat)
            lon_rad = math.radians(lon)
            kaaba_lat_rad = math.radians(kaaba_lat)
            kaaba_lon_rad = math.radians(kaaba_lon)

            delta_lon = kaaba_lon_rad - lon_rad
            x = math.sin(delta_lon)
            y = math.cos(lat_rad) * math.tan(kaaba_lat_rad) - math.sin(lat_rad) * math.cos(delta_lon)

            qibla_rad = math.atan2(x, y)
            qibla_deg = (math.degrees(qibla_rad) + 360) % 360

            if request.user.is_authenticated:
                QiblaRequest.objects.create(
                    user=request.user,
                    latitude=lat,
                    longitude=lon,
                    qibla_direction=qibla_deg
                )

            return Response({'qibla_direction': qibla_deg}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)