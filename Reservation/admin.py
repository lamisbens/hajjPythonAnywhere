from django.contrib import admin

# Register your models here.
from .models import Rituel, Reservation, Itineraire, Pelerin,ScannedQRCode, Alerte, Hotel, Emplacement, QiblaRequest, Traduction, Communication, HeurePriere, AttractionTouristique


@admin.register(Rituel)
class RituelAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_rituel', 'ordre']
    ordering = ['type_rituel', 'ordre']

admin.site.register(Reservation)
admin.site.register(Emplacement)
admin.site.register(ScannedQRCode)
admin.site.register(Alerte)
admin.site.register(Hotel)
admin.site.register(Pelerin)
admin.site.register(Itineraire)
admin.site.register(QiblaRequest)
admin.site.register(Communication)
admin.site.register(HeurePriere)
admin.site.register(AttractionTouristique)
admin.site.register(Traduction)