# Generated by Django 5.1.1 on 2024-09-24 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0028_artcollection_is_featured_artfiletag_is_featured"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artcollection",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]
