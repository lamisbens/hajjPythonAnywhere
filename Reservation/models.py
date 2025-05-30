from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
from Session.models import Pelerin, Hotel, Traduction, QiblaRequest, Communication, HeurePriere, AttractionTouristique, Traduction


class Reservation(models.Model):
    pelerin = models.ForeignKey(Pelerin, on_delete=models.CASCADE, related_name='reservations')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reservations')
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return f"Réservation de {self.pelerin.user.username} à {self.hotel.nom}"


class Alerte(models.Model):
    resolue = models.BooleanField(default=False)
    ALERT_CHOICES = (
        ('perdu', 'Perdu'),
        ('urgence', 'Urgence Médicale'),
        ('chute', 'Chute'),
    )
    pelerin = models.ForeignKey(Pelerin, on_delete=models.CASCADE, related_name='alertes')
    type_alerte = models.CharField(max_length=10, choices=ALERT_CHOICES)
    description = models.TextField()
    statut = models.CharField(max_length=20, default='En attente')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerte de {self.pelerin.user.username} - {self.type_alerte}"


class Itineraire(models.Model):
    pelerin = models.ForeignKey(Pelerin, on_delete=models.CASCADE, related_name='itineraires')
    date = models.DateField()
    lieu = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Itinéraire pour {self.pelerin.user.username}"


class Emplacement(models.Model):
    pelerin = models.ForeignKey(Pelerin, on_delete=models.CASCADE, related_name='emplacements')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Emplacement de {self.pelerin.user.username}"

    @staticmethod
    def update_location(pelerin, latitude, longitude):
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            raise ValidationError("Les coordonnées doivent être des nombres valides.")

        emplacement, _ = Emplacement.objects.update_or_create(
            pelerin=pelerin,
            defaults={"latitude": latitude, "longitude": longitude}
        )
        return emplacement


class ScannedQRCode(models.Model):
    code = models.CharField(max_length=255)
    scanned_at = models.DateTimeField(auto_now_add=True)


class Rituel(models.Model):
    TYPE_CHOICES = (
        ('hajj', 'Hajj'),
        ('omra', 'Omra'),
    )

    titre = models.CharField(max_length=255)
    description = models.TextField()
    ordre = models.PositiveIntegerField()
    type_rituel = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_rituel.capitalize()} - {self.ordre}. {self.titre}"


