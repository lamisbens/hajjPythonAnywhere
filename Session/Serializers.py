from rest_framework import serializers
from django.contrib.auth import get_user_model

from Session.models import Communication, HeurePriere, AttractionTouristique, Hotel, Pelerin, User


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


# ---------- Pelerin Serializer ----------
class PelerinSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Pelerin
        fields = ['id', 'user', 'badge', 'periode_hajj', 'maladies', 'contact_urgence']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_id = user_data.get('id', None)

        if user_id:
            # Mise à jour du user existant
            try:
                user = User.objects.get(id=user_id)
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                user.save()
            except User.DoesNotExist:
                raise serializers.ValidationError(f"User with id {user_id} does not exist.")
        else:
            # Création d'un nouveau user
            user = User.objects.create(**user_data)

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