from django.urls import path
from .views import (
    ListItinerariesView,
    CreateItineraryView,
    RetrieveUpdateDeleteItineraryView,
    CreateItineraryStepView,
    RetrieveUpdateDeleteItineraryStepView
)

urlpatterns = [
    path('itineraries/', ListItinerariesView.as_view(), name='itinerary-list'),
    path('itineraries/create/', CreateItineraryView.as_view(), name='itinerary-create'),
    path('itineraries/<int:pk>/', RetrieveUpdateDeleteItineraryView.as_view(), name='itinerary-detail'),
    path('itineraries/<int:itinerary_id>/steps/create/', CreateItineraryStepView.as_view(), name='itinerarystep-create'),
    path('itinerarysteps/<int:pk>/', RetrieveUpdateDeleteItineraryStepView.as_view(), name='itinerarystep-detail'),
]

