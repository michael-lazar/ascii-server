# Generated by Django 4.2.11 on 2024-09-03 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0006_alter_artfile_options_alter_artfile_filesize"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artfile",
            name="file_extension",
            field=models.CharField(blank=True, db_index=True, max_length=20),
        ),
    ]