# Generated by Django 5.1.1 on 2024-09-22 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0021_alter_gallery_options_alter_gallery_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="gallery",
            name="visible",
            field=models.BooleanField(default=False),
        ),
    ]