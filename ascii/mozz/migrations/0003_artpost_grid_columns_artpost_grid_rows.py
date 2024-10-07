# Generated by Django 5.1.1 on 2024-10-02 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mozz", "0002_alter_artpost_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="artpost",
            name="grid_columns",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="artpost",
            name="grid_rows",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
