from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from Session.models import Communication, HeurePriere, AttractionTouristique, Hotel, Pelerin, User
from .Serializers import (
    UserSerializer, PelerinSerializer,
    HotelSerializer, AttractionTouristiqueSerializer,
    HeurePriereSerializer, CommunicationSerializer
)


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


class UserInfo(APIView):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Retrieve the user information you need
        data = {
            'username': user.username,
            'email': user.email,
            # Add other fields as needed
        }
        return Response(UserSerializer(user).data)


# ----------- User ViewSet -----------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [IsAuthenticated]


# ----------- Pèlerin ViewSet -----------
class PelerinViewSet(viewsets.ModelViewSet):
    queryset = Pelerin.objects.select_related('user').all()
    serializer_class = PelerinSerializer
    #permission_classes = [IsAuthenticated]


# ----------- Hôtel ViewSet -----------
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    #permission_classes = [IsAuthenticated]


# ----------- Attraction Touristique ViewSet -----------
class AttractionTouristiqueViewSet(viewsets.ModelViewSet):
    queryset = AttractionTouristique.objects.all()
    serializer_class = AttractionTouristiqueSerializer
    #permission_classes = [IsAuthenticated]


# ----------- Heure de Prière ViewSet -----------
class HeurePriereViewSet(viewsets.ModelViewSet):
    queryset = HeurePriere.objects.all()
    serializer_class = HeurePriereSerializer
    #permission_classes = [IsAuthenticated]


# ----------- Communication ViewSet -----------
class CommunicationViewSet(viewsets.ModelViewSet):
    serializer_class = CommunicationSerializer
    #permission_classes = [IsAuthenticated]

    """def get_queryset(self):
        user = self.request.user
        return Communication.objects.filter(sender=user) | Communication.objects.filter(receiver=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)"""
