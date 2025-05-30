import requests
from rest_framework import serializers
from django.contrib.auth import get_user_model

from Reservation.models import Emplacement, RituelSteps, Alerte
from Session.models import Communication, HeurePriere, AttractionTouristique, Hotel, Pelerin, User, Traduction, QiblaRequest
from datetime import datetime



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'bracelet_id', 'telephone', 'bracelet_number', 'status', 'type', 'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


import math


def get_qibla_direction(latitude, longitude):

    # Kaaba's coordinates in Mecca (latitude, longitude)
    mecca_lat = 21.3891
    mecca_lon = 39.8579

    # Convert degrees to radians
    user_lat_rad = math.radians(latitude)
    user_lon_rad = math.radians(longitude)
    mecca_lat_rad = math.radians(mecca_lat)
    mecca_lon_rad = math.radians(mecca_lon)

    # Calculate the difference in longitude
    delta_lon = mecca_lon_rad - user_lon_rad

    # Calculate the Qibla angle using the formula
    y = math.sin(delta_lon)
    x = math.cos(user_lat_rad) * math.tan(mecca_lat_rad) - math.sin(user_lat_rad) * math.cos(delta_lon)
    qibla_angle_rad = math.atan2(y, x)

    # Convert radians to degrees and normalize (0° to 360°)
    qibla_angle_deg = math.degrees(qibla_angle_rad)
    qibla_angle_deg = (qibla_angle_deg + 360) % 360  # Ensure positive value

    return qibla_angle_deg


def get_next_prayer(latitude, longitude):
    # Fetch prayer times from Aladhan API
    url = f"http://api.aladhan.com/v1/timings?latitude={latitude}&longitude={longitude}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    timings = data["data"]["timings"]

    # Define the prayer order (Fajr, Dhuhr, Asr, Maghrib, Isha)
    prayer_order = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

    # Get current time in 24-hour format (e.g., "14:30")
    current_time = datetime.now().strftime("%H:%M")

    # Find the next prayer
    for prayer in prayer_order:
        prayer_time = timings.get(prayer)
        if prayer_time and prayer_time > current_time:
            return {
                "next_prayer": prayer,
                "time": prayer_time,
                "qibla_direction": get_qibla_direction(latitude, longitude)  # Optional
            }

    # If all prayers passed, return the first prayer of the next day (Fajr)
    return {
        "next_prayer": "Fajr (Tomorrow)",
        "time": timings["Fajr"],
        "qibla_direction": get_qibla_direction(latitude, longitude)  # Optional
    }



# ---------- Pelerin Serializer ----------
class PelerinSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Pelerin
        fields = "__all__"#['id', 'user', 'badge', 'periode_hajj', 'maladies', 'contact_urgence', 'guide']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        """request = self.context.get('request')
        latitude = request.query_params.get('lat')  # or request.data.get('lat')
        longitude = request.query_params.get('lng')




        try:
            rituel = RituelSteps.objects.filter(
                        pelerin=instance,
                        statut=False
                    ).order_by('-id').first().rituel.titre
        except Exception:
            rituel = 'Completé'


        liste_alert = Alerte.objects.filter(pelerin = instance, resolue=False).order_by('-id')
        alertes = []
        for elem in liste_alert:
            alertes.append({
                'type_alerte': elem.type_alerte,
                'description': elem.description
            })

        representation['rituel'] = rituel
        representation['priere'] = get_next_prayer(float(latitude), float(longitude))
        representation['alertes'] = alertes"""


        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)

        user.save()



        pelerin = Pelerin.objects.create(user=user, **validated_data)
        return pelerin

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# ---------- Hotel Serializer ----------
class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'nom', 'adresse', 'latitude', 'longitude', 'capacite']

# ---------- AttractionTouristique Serializer ----------
class AttractionTouristiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttractionTouristique
        fields = ['id', 'nom', 'description', 'latitude', 'longitude', 'emplacement']

# ---------- HeurePriere Serializer ----------
class HeurePriereSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeurePriere
        fields = ['id', 'ville', 'fajr', 'dohr', 'asr', 'maghrib', 'isha', 'date']

# ---------- Communication Serializer ----------
class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp']

# ---------- TraductionSerializer ----------
class TraductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traduction
        fields = ['texte_original', 'texte_traduit', 'langue_source', 'langue_cible']

# ---------- QiblaRequestSerializer ----------
class QiblaRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = QiblaRequest
        fields = ['latitude', 'longitude', 'qibla_direction', 'user', 'requested_at']
