# Generated by Django 5.0 on 2024-03-07 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0002_vaccine_recipient_taken_dose'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vaccine',
            name='next_dose',
        ),
        migrations.AddField(
            model_name='vaccine_recipient',
            name='next_dose',
            field=models.DateField(blank=True, null=True),
        ),
    ]
