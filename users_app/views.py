from rest_framework.views import APIView
from .models import User, Preference
from rest_framework import generics, status
from .serializers import UserSerializer, PreferenceSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class PreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data.get('preferences', [])
        if not data:
            return Response({'error': 'No preferences data provided'}, status=status.HTTP_400_BAD_REQUEST)

        for pref_data in data:
            preference_type = pref_data.get('preference_type')
            if not preference_type:
                return Response({'error': 'Preference type not provided'}, status=status.HTTP_400_BAD_REQUEST)

            preference, created = Preference.objects.update_or_create(
                user=user,
                preference_type=preference_type,
                defaults={'preference_value': pref_data.get('preference_value', '')}
            )

            if not created:
                print(f"Preference {preference_type} already exists and was updated for user {user.username}.")
            else:
                print(f"Preference {preference_type} created for user {user.username}.")

        return Response({'message': 'Preferences processed successfully.'}, status=status.HTTP_201_CREATED)

    def update(self, request):
        """
        Aggiorna le preferenze esistenti per l'utente.
        """
        user = request.user
        data = request.data.get('preferences', [])
        if not data:
            return Response({'error': 'No preferences data provided'}, status=status.HTTP_400_BAD_REQUEST)

        for pref_data in data:
            preference_type = pref_data.get('preference_type')
            if not preference_type:
                return Response({'error': 'Preference type not provided'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                preference = Preference.objects.get(user=user, preference_type=preference_type)
            except Preference.DoesNotExist:
                print(f"Preference with type '{preference_type}' for user '{user.id}' not found.")  # Log per debug
                return Response({'error': f'Preference type {preference_type} not found for user {user.username}'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = PreferenceSerializer(preference, data=pref_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print(f"Preference {preference_type} updated successfully.")  # Log per debug
            else:
                print(f"Validation errors for {preference_type}: {serializer.errors}")  # Log per debug
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Preferences updated successfully.'}, status=status.HTTP_200_OK)


class DeletePreferenceView(generics.DestroyAPIView):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
    permission_classes = (IsAuthenticated,)


class GetUserPreferencesView(generics.ListAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Preference.objects.filter(user=user)
