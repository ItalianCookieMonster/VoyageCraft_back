from django.urls import path

from destinations.views import DestinationRecommendationView

urlpatterns = [
    path('/recommended-destinations', DestinationRecommendationView.as_view(), name="recommended-destinations"),
]


