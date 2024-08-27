from django.urls import path
from . import views


urlpatterns = [
    path('preferences/', views.CreatePreferenceView.as_view(), name="preferences"),
    path('preferences/delete<int:pk>/', views.DeletePreferenceView.as_view(), name="delete_preference"),
    path('preferences/update<int:pk>/', views.UpdatePreferenceView.as_view(), name="update_preference"),
]