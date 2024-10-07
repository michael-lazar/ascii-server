# Generated by Django 5.1.1 on 2024-10-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mozz", "0007_artpost_visible"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artpost",
            name="file_type",
            field=models.CharField(
                choices=[("text", "Plaintext"), ("xbin", "XBin"), ("image", "Image")], max_length=16
            ),
        ),
    ]