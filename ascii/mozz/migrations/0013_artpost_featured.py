# Generated by Django 5.1.1 on 2024-10-09 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mozz", "0012_alter_artpost_file_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="artpost",
            name="featured",
            field=models.BooleanField(default=False),
        ),
    ]
