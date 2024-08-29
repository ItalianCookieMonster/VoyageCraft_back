from django.urls import path
from .views import (
    ListItinerariesView,
    CreateItineraryView,
    RetrieveUpdateDeleteItineraryView,
    CreateItineraryStepView,
    RetrieveUpdateDeleteItineraryStepView
)

urlpatterns = [
    path('itineraries/', ListItinerariesView.as_view(), name='list_itineraries'),
    path('itineraries/create/', CreateItineraryView.as_view(), name='create_itinerary'),
    path('itineraries/<int:pk>/', RetrieveUpdateDeleteItineraryView.as_view(), name='itinerary_detail'),
    path('itineraries/<int:itinerary_id>/steps/create/', CreateItineraryStepView.as_view(), name='create_itinerary_step'),
    path('steps/<int:pk>/', RetrieveUpdateDeleteItineraryStepView.as_view(), name='itinerary_step_detail'),
]
