# Generated by Django 4.2.11 on 2024-08-21 03:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0003_alter_artfile_options_artfile_file_extension_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="artfile",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="artpack",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
