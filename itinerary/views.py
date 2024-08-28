from rest_framework import generics
from .models import Itinerary
from .serializer import ItinerarySerializer

class CreateItineraryView(generics.CreateAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

class RetrieveUpdateDeleteItineraryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

class ListItinerariesView(generics.ListAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

