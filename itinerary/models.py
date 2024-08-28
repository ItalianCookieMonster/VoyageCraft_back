from django.db import models
from users_app.models import User
from destinations.models import Destination, Activity
class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class ItineraryStep(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    step_order = models.IntegerField()
    stay_duration_hours = models.FloatField()
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Step {self.step_order} of {self.itinerary.name}"

