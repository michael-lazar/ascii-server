# Generated by Django 5.1.1 on 2024-09-22 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0020_gallery"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="gallery",
            options={"ordering": ["-id"], "verbose_name_plural": "Galleries"},
        ),
        migrations.AlterField(
            model_name="gallery",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
