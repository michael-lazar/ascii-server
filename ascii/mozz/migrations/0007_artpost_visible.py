# Generated by Django 5.1.1 on 2024-10-03 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mozz", "0006_remove_artpost_grid_column_span_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="artpost",
            name="visible",
            field=models.BooleanField(default=True),
        ),
    ]