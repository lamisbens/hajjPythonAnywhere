# Generated by Django 5.2.1 on 2025-05-30 22:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Session', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pelerin',
            name='guide',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Session.pelerin'),
        ),
        migrations.AddField(
            model_name='pelerin',
            name='hotel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Session.hotel'),
        ),
    ]
