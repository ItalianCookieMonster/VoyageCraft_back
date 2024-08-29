# Generated by Django 5.1 on 2024-08-28 13:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('destinations', '0004_activity_created_at_activity_updated_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='destinations.destination')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItineraryStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_order', models.IntegerField()),
                ('stay_duration_hours', models.FloatField()),
                ('note', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='destinations.activity')),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itinerary.itinerary')),
            ],
        ),
    ]
