# Generated by Django 4.2.11 on 2024-08-04 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0003_alter_artfile_options_alter_artfile_artist_tags_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="artpack",
            name="fileid",
        ),
        migrations.AddField(
            model_name="artfile",
            name="is_fileid",
            field=models.BooleanField(default=False),
        ),
    ]