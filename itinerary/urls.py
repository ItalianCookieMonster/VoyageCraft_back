from django.urls import path
from . import views

urlpatterns = [
    # Crear un nuevo itinerario
    path('create/', views.CreateItineraryView.as_view(), name="create_itinerary"),

    # Obtener, actualizar o eliminar un itinerario específico por su ID
    path('<int:pk>/', views.RetrieveUpdateDeleteItineraryView.as_view(), name="itinerary_detail"),

    # Listar todos los itinerarios
    path('', views.ListItinerariesView.as_view(), name="list_itineraries"),
]

urlpatterns = [
    # Create a new itinerary step
    path('create/', views.CreateItineraryStepView.as_view(), name="create_itinerary_step"),

    # Retrieve, update or delete a specific itinerary step by its ID
    path('<int:pk>/', views.RetrieveUpdateDeleteItineraryStepView.as_view(), name="itinerary_step_detail"),

    # List all itinerary steps (optional)
    path('', views.ListItineraryStepsView.as_view(), name="list_itinerary_steps"),
]
