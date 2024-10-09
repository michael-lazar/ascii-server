# Generated by Django 5.1.1 on 2024-10-09 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mozz", "0011_scrollfile_alter_artpostattachment_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artpost",
            name="file_type",
            field=models.CharField(
                choices=[("text", "Plain text"), ("xbin", "XBin"), ("other", "Other")],
                max_length=16,
            ),
        ),
    ]
