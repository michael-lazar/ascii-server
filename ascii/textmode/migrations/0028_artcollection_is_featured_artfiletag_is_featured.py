# Generated by Django 5.1.1 on 2024-09-24 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0027_artcollection_artcollectionmapping_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="artcollection",
            name="is_featured",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="artfiletag",
            name="is_featured",
            field=models.BooleanField(default=False),
        ),
    ]
