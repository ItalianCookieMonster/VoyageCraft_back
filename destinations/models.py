from django.db import models
from django.utils.text import slugify


class Destination(models.Model):
    TYPE_CHOICES = [
        ('POI', 'Point of Interest'),
        ('City', 'City'),
        ('Region', 'Region'),
    ]

    LANDSCAPE_CHOICES = [
        ('Beach', 'Beach'),
        ('Mountains', 'Mountains'),
        ('Forest', 'Forest'),
        ('Desert', 'Desert'),
        ('Urban', 'Urban/Cities'),
        ('Countryside', 'Countryside'),
        ('Lakes/Rivers', 'Lakes/Rivers'),
    ]

    TOURISM_TYPE_CHOICES = [
        ('Cultural', 'Cultural (Museums, historical sites)'),
        ('Adventure', 'Adventure (Hiking, extreme sports)'),
        ('Relaxation', 'Relaxation (Beaches, spas)'),
        ('Nature', 'Nature (National parks, wildlife)'),
        ('Nightlife', 'Nightlife (Bars, clubs)'),
        ('Family-friendly', 'Family-friendly'),
        ('Shopping', 'Shopping'),
    ]

    COST_LEVEL_CHOICES = [
        ('Low', 'Low (Backpacking, hostels)'),
        ('Medium', 'Medium (Hotels, mid-range restaurants)'),
        ('High', 'High (Luxury hotels, fine dining)'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    description = models.TextField(blank=True)
    photo_url = models.URLField(max_length=500, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='sub_destinations')
    landscape = models.CharField(max_length=20, choices=LANDSCAPE_CHOICES)
    tourism_type = models.CharField(max_length=50, choices=TOURISM_TYPE_CHOICES)
    cost_level = models.CharField(max_length=10, choices=COST_LEVEL_CHOICES)
    family_friendly = models.BooleanField(default=False)
    accessibility = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'destinations'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.type}")
        super(Destination, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Activity(models.Model):
    WEATHER_CHOICES = [
        ('Sunny', 'Sunny'),
        ('Rainy', 'Rainy'),
        ('Snowy', 'Snowy'),
        ('Cloudy', 'Cloudy'),
        ('Windy', 'Windy'),
        ('Any', 'Any'),  # Suitable in any weather
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    suitable_weather = models.CharField(max_length=20, choices=WEATHER_CHOICES, default='Any')
    description = models.TextField(blank=True)
    duration_hours = models.DecimalField(max_digits=4, decimal_places=2)  # Supports fractional hours, e.g., 1.5 hours
    pet_friendly = models.BooleanField(default=False)
    family_friendly = models.BooleanField(default=False)
    accessibility = models.BooleanField(default=False)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='activities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'activities'


class WeatherData(models.Model):
    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]

    WEATHER_CHOICES = [
        ('Sunny', 'Sunny'),
        ('Rainy', 'Rainy'),
        ('Cold', 'Cold'),
        ('Cloudy', 'Cloudy'),
        ('Windy', 'Windy'),
        ('Hot', 'Hot'),
    ]

    id = models.AutoField(primary_key=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='weather_data')
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    weather = models.CharField(max_length=20, choices=WEATHER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.destination.name} - {self.month} - {self.weather}"

    class Meta:
        db_table = 'weather_data'
