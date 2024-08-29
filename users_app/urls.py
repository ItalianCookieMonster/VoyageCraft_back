from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # User registration and authentication
    path('register/', views.CreateUserView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User update
    path('user/', views.RetrieveUpdateUserView.as_view(), name="update_user"),

    # Preferences management
    path('preferences/', views.ManagePreferencesView.as_view(), name="preferences"),
    path('preferences/delete/<int:pk>/', views.DeletePreferenceView.as_view(), name="delete_preference"),
    path('preferences/get/', views.GetUserPreferencesView.as_view(), name="get_preferences"),

    # DRF browsable API login
    path('auth/', include('rest_framework.urls')),
]

