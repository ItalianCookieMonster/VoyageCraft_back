from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from voyage_craft import settings


class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Preference(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preferences'
    )
    preference_type = models.CharField(max_length=255)
    preference_value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.preference_type}: {self.preference_value}"

    class Meta:
        verbose_name = "Preference"
        verbose_name_plural = "Preferences"
        ordering = ['-created_at']
        db_table = 'user_preferences'
        permissions = [
            ("can_change_preference_type", "Can change the preference type"),
        ]
