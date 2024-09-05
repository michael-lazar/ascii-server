# Generated by Django 4.2.11 on 2024-09-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0010_artfile_comments"),
    ]

    operations = [
        migrations.AddField(
            model_name="artfile",
            name="font_name",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="artfile",
            name="comments",
            field=models.TextField(blank=True, db_index=True),
        ),
    ]
