from django.db.models import Q

from users_app.models import Preference


def get_user_preferences(user) -> Preference:
    return Preference.objects.filter(user=user)


def build_strict_query(user_preferences) -> Q:
    strict_query = Q()

    for pref in user_preferences:
        if pref.preference_type == 'accessibility':
            strict_query &= Q(accessibility=pref.preference_value.strip().lower() == 'true')
        elif pref.preference_type == 'family_friendly':
            strict_query &= Q(family_friendly=pref.preference_value.strip().lower() == 'true')

    return strict_query


def build_type_query(user_preferences) -> Q:
    type_query = Q()
    has_duration_pref = False

    for pref in user_preferences:
        if pref.preference_type == 'travel_duration':
            has_duration_pref = True
            type_query |= build_duration_query(pref.preference_value)

    return type_query | add_default_type_query(has_duration_pref)


def build_flexible_query(user_preferences) -> Q:
    flexible_query = Q()
    flexible_or_query = Q()
    important_pref_applied = False

    for pref in user_preferences:
        if pref.preference_type == 'preferred_climate':
            flexible_query &= Q(weather_data__weather=pref.preference_value)
            important_pref_applied = True
        elif pref.preference_type == 'landscape':
            flexible_or_query |= Q(landscape=pref.preference_value)
        elif pref.preference_type == 'tourism_type':
            flexible_or_query |= Q(tourism_type=pref.preference_value)
        elif pref.preference_type == 'cost_level':
            flexible_query &= Q(cost_level=pref.preference_value)
            important_pref_applied = True

    final_query = flexible_query & flexible_or_query

    if not important_pref_applied:
        final_query &= Q(id__lt=0)

    return final_query


def build_duration_query(duration_pref: str) -> Q:
    if duration_pref in ['1-3 days', '4-7 days']:
        return Q(type__in=['City', 'POI'])
    elif duration_pref in ['1-2 weeks', '2 weeks or more']:
        return Q(type__in=['City', 'Region'])
    return Q()


def add_default_type_query(has_duration_pref: bool) -> Q:
    if not has_duration_pref:
        return Q(type__in=['City', 'POI', 'Region'])
    return Q()
