from rest_framework import routers
from Session.views import UserViewSet, PelerinViewSet, HotelViewSet, AttractionTouristiqueViewSet, HeurePriereViewSet, CommunicationViewSet
routerelem = routers.DefaultRouter()
from Reservation.views import ReservationViewSet, AlerteViewSet, ItineraireViewSet, EmplacementViewSet

routerelem.register('user', UserViewSet, basename='user')
routerelem.register('pelerin', PelerinViewSet, basename='pelerin')
routerelem.register('hotel', HotelViewSet, basename='hotel')
routerelem.register('attraction', AttractionTouristiqueViewSet, basename='attraction')
routerelem.register('heurep', HeurePriereViewSet, basename='heurep')
routerelem.register('communication', CommunicationViewSet, basename='communication')
routerelem.register('reservations', ReservationViewSet, basename='reservation')
routerelem.register('alertes', AlerteViewSet, basename='alerte')
routerelem.register('itineraires', ItineraireViewSet, basename='itineraire')
routerelem.register('emplacements', EmplacementViewSet, basename='emplacement')