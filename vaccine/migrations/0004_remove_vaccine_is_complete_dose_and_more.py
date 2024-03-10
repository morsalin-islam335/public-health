# Generated by Django 5.0 on 2024-03-07 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0003_remove_vaccine_next_dose_vaccine_recipient_next_dose'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaccine',
            name='is_complete_dose',
        ),
        migrations.AddField(
            model_name='vaccine_recipient',
            name='is_complete_dose',
            field=models.BooleanField(default=False),
        ),
    ]