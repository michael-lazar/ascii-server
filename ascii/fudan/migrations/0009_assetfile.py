# Generated by Django 4.2.11 on 2024-05-04 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fudan", "0008_scratchfile"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssetFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("slug", models.SlugField(unique=True)),
                ("file", models.FileField(upload_to="")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
