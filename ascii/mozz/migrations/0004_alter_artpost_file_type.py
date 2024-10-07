# Generated by Django 5.1.1 on 2024-10-02 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mozz", "0003_artpost_grid_columns_artpost_grid_rows"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artpost",
            name="file_type",
            field=models.CharField(
                choices=[("text", "Text"), ("xbin", "XBin"), ("image", "Image")], max_length=16
            ),
        ),
    ]
