from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Itinerary, ItineraryStep
from .serializer import ItinerarySerializer, ItineraryStepSerializer


class ListItinerariesView(generics.ListAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticated]


class CreateItineraryView(generics.CreateAPIView):
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticated]

class RetrieveUpdateDeleteItineraryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticated]


class CreateItineraryStepView(generics.CreateAPIView):
    serializer_class = ItineraryStepSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        itinerary_id = self.kwargs.get('itinerary_id')
        itinerary = Itinerary.objects.get(id=itinerary_id)
        serializer.save(itinerary=itinerary)


class RetrieveUpdateDeleteItineraryStepView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ItineraryStep.objects.all()
    serializer_class = ItineraryStepSerializer
    permission_classes = [IsAuthenticated]
