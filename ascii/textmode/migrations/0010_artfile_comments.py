# Generated by Django 4.2.11 on 2024-09-04 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0009_alter_artfile_filetype"),
    ]

    operations = [
        migrations.AddField(
            model_name="artfile",
            name="comments",
            field=models.CharField(blank=True, db_index=True, max_length=20),
        ),
    ]