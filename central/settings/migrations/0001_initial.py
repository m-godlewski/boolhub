# Generated by Django 4.2.16 on 2024-11-28 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature_min', models.FloatField(default=19.0)),
                ('temperature_max', models.FloatField(default=27.0)),
                ('notify_temperature', models.BooleanField(default=True)),
                ('humidity_min', models.IntegerField(default=20)),
                ('humidity_max', models.IntegerField(default=85)),
                ('notify_humidity', models.BooleanField(default=True)),
                ('aqi_threshold', models.IntegerField(default=50)),
                ('notify_aqi', models.BooleanField(default=True)),
                ('network_overload_threshold', models.IntegerField(default=10)),
                ('notify_network_overload', models.BooleanField(default=True)),
                ('notify_unknown_device', models.BooleanField(default=True)),
                ('health_threshold', models.IntegerField(default=15)),
                ('notify_health', models.BooleanField(default=True)),
                ('weather_api_url', models.CharField(blank=True, max_length=250, null=True)),
                ('weather_api_latitude', models.CharField(blank=True, max_length=250, null=True)),
                ('weather_api_longitude', models.CharField(blank=True, max_length=250, null=True)),
                ('weather_api_token', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'db_table': 'settings',
            },
        ),
    ]
