from django.contrib import admin
from .models import User, Preference

# Register your models here.

admin.site.register(User)


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'preference_type', 'preference_value', 'created_at', 'updated_at')
    search_fields = ('user__username', 'preference_type')
