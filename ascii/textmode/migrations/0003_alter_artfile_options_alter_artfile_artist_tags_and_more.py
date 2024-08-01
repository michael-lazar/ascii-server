# Generated by Django 4.2.11 on 2024-08-01 20:34

import ascii.textmode.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0002_alter_artisttag_options_alter_artpack_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="artfile",
            options={"ordering": ["name"]},
        ),
        migrations.AlterField(
            model_name="artfile",
            name="artist_tags",
            field=models.ManyToManyField(
                blank=True, related_name="artfiles", to="textmode.artisttag"
            ),
        ),
        migrations.AlterField(
            model_name="artfile",
            name="content_tags",
            field=models.ManyToManyField(
                blank=True, related_name="artfiles", to="textmode.contenttag"
            ),
        ),
        migrations.AlterField(
            model_name="artfile",
            name="group_tags",
            field=models.ManyToManyField(
                blank=True, related_name="artfiles", to="textmode.grouptag"
            ),
        ),
        migrations.AlterField(
            model_name="artfile",
            name="image_x2",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=ascii.textmode.models.upload_to_x2,
                verbose_name="Image (x2)",
            ),
        ),
        migrations.AlterField(
            model_name="artfile",
            name="pack",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="artfiles",
                to="textmode.artpack",
            ),
        ),
        migrations.AlterField(
            model_name="artpack",
            name="fileid",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="textmode.artfile",
                verbose_name="File ID",
            ),
        ),
    ]
