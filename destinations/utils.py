from django.db.models import Q
from users_app.models import Preference


def build_destination_query(user):
    preferences = Preference.objects.filter(user=user)

    # Verifica se le preferenze esistono
    if not preferences.exists():
        print(f"Missing preference data for user {user.username}. Skipping.")
        return None

    query = Q()

    # Mappatura dei tipi di preferenze ai campi del modello Destination
    preference_mapping = {
        'climate': 'climate',
        'landscape': 'landscape',
        'tourism_type': 'tourism_type',
        'trip_duration': 'trip_duration',
        'cost_level': 'cost_level',
        'accessibility': 'accessibility',
        'family_friendly': 'family_friendly'
    }

    for preference in preferences:
        field = preference_mapping.get(preference.preference_type)
        if field:
            if field in ['accessibility', 'family_friendly']:
                query_value = preference.preference_value.lower() == 'true'
                query |= Q(**{field: query_value})
            else:
                query |= Q(**{field: preference.preference_value})
        else:
            print(f"Unrecognized preference type {preference.preference_type} for user {user.username}. Skipping.")

    if query == Q():
        print(f"No valid preferences found for user {user.username}.")
        return None

    return query