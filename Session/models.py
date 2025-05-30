from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    bracelet_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    bracelet_number = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=True)

    TYPE_CHOICES = (
        ('pelerin', 'Pèlerin'),
        ('guide', 'Guide'),
        ('admin', 'Administrateur'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="pelerin")

    def __str__(self):
        return self.username



class Hotel(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    capacite = models.IntegerField()

    def __str__(self):
        return self.nom

class Pelerin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pelerin')
    badge = models.CharField(max_length=100, unique=True)
    periode_hajj = models.CharField(max_length=50)
    maladies = models.TextField(blank=True, null=True)
    contact_urgence = models.CharField(max_length=20)

    guide = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='guide')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Pèlerin"
        verbose_name_plural = "Pèlerins"

    def __str__(self):
        return self.user.username


class AttractionTouristique(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    emplacement = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class HeurePriere(models.Model):
    ville = models.CharField(max_length=100)
    fajr = models.TimeField()
    dohr = models.TimeField()
    asr = models.TimeField()
    maghrib = models.TimeField()
    isha = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return f"Heures de prière pour {self.ville} le {self.date}"


class Communication(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_communications')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_communications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Traduction(models.Model):
    texte_original = models.TextField()
    texte_traduit = models.TextField()
    langue_source = models.CharField(max_length=10)
    langue_cible = models.CharField(max_length=10)


class QiblaRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    qibla_direction = models.FloatField()
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Qibla direction {self.qibla_direction}° for user {self.user} at {self.requested_at}"
