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


def _create_preference(preference_type, preference_value, user):
    serializer = PreferenceSerializer(data={
        "preference_type": preference_type,
        "preference_value": preference_value,
        "user": user.id
    })
    if serializer.is_valid():
        serializer.save(user=user)
        logger.info(f"Created new preference {preference_type} for user {user.username}.")
        return True, None
    else:
        logger.warning(
            f"Validation failed for creating preference {preference_type} with value {preference_value}: {serializer.errors}")
        return False, serializer.errors


class ManagePreferencesView(generics.GenericAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        preferences_data = request.data.get('preferences', [])
        user = request.user

        try:
            existing_preferences = self._get_existing_preferences(user)
            errors = []

            for pref_data in preferences_data:
                preference_type, preference_value = self._extract_preference_data(pref_data)
                if not preference_type or not preference_value:
                    logger.warning(f"Missing preference data for user {user.username}. Skipping.")
                    continue

                success, error = self._create_or_update_preference(user, preference_type, preference_value,
                                                                   existing_preferences)
                if not success:
                    errors.append(error)

            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"Preferences processed successfully for user {user.username}.")
            return Response({"message": "Preferences processed successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"An unexpected error occurred for user {user.username}: {e}")
            return Response({"error": "An unexpected error occurred. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _get_existing_preferences(self, user):
        return {pref.preference_type: pref for pref in Preference.objects.filter(user=user)}

    def _extract_preference_data(self, pref_data):
        return pref_data.get('preference_type'), pref_data.get('preference_value')

    def _create_or_update_preference(self, user, preference_type, preference_value, existing_preferences):
        try:
            if preference_type in existing_preferences:
                preference = existing_preferences[preference_type]
                return self._update_preference(preference, preference_value, user)
            else:
                return _create_preference(preference_type, preference_value, user)
        except Exception as e:
            logger.error(f"Error processing preference {preference_type} for user {user.username}: {e}")
            return False, f"Error processing preference {preference_type}: {str(e)}"

    def _update_preference(self, preference, preference_value, user):
        serializer = PreferenceSerializer(preference, data={"preference_value": preference_value}, partial=True)
        if serializer.is_valid():
            serializer.save(user=user)
            logger.info(f"Updated preference {preference.preference_type} for user {user.username}.")
            return True, None
        else:
            logger.warning(
                f"Validation failed for updating preference {preference.preference_type} with value {preference_value}: {serializer.errors}")
            return False, serializer.errors


class DeletePreferenceView(generics.DestroyAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = (IsAuthenticated,)


class GetUserPreferencesView(generics.ListAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Preference.objects.filter(user=user)
