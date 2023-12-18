# Generated by Django 4.2.1 on 2023-10-17 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_alter_device_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='token',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='category',
            field=models.CharField(choices=[('network', 'Urządzenie sieciowe'), ('computer', 'PC/Laptop'), ('smartphone', 'Smartfon/Komórka'), ('tablet', 'Tablet/Czytnik'), ('printer', 'Drukarka'), ('tv', 'TV/Odtwarzacz multimedialny'), ('light', 'Oświetlenie'), ('air', 'Oczyszczacz powietrza/termometr'), ('console', 'Konsola'), ('other', 'Inne')], max_length=50),
        ),
    ]