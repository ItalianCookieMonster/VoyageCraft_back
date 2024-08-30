# Generated by Django 5.1 on 2024-08-28 09:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destinations', '0002_destination_slug_alter_destination_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('suitable_weather', models.CharField(choices=[('Sunny', 'Sunny'), ('Rainy', 'Rainy'), ('Snowy', 'Snowy'), ('Cloudy', 'Cloudy'), ('Windy', 'Windy'), ('Any', 'Any')], default='Any', max_length=20)),
                ('description', models.TextField(blank=True)),
                ('duration_hours', models.DecimalField(decimal_places=2, max_digits=4)),
                ('pet_friendly', models.BooleanField(default=False)),
                ('family_friendly', models.BooleanField(default=False)),
                ('accessibility', models.BooleanField(default=False)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='destinations.destination')),
            ],
            options={
                'db_table': 'activities',
            },
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20)),
                ('weather', models.CharField(choices=[('Sunny', 'Sunny'), ('Rainy', 'Rainy'), ('Cold', 'Cold'), ('Cloudy', 'Cloudy'), ('Windy', 'Windy'), ('Hot', 'Hot')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weather_data', to='destinations.destination')),
            ],
            options={
                'db_table': 'weather_data',
            },
        ),
    ]
