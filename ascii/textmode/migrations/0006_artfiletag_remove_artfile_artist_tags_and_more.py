# Generated by Django 4.2.11 on 2024-08-15 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0005_alter_artfile_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtFileTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[("artist", "Artist"), ("content", "Content"), ("group", "Group")],
                        db_index=True,
                        max_length=20,
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=100)),
            ],
            options={
                "ordering": ["category", "name"],
            },
        ),
        migrations.RemoveField(
            model_name="artfile",
            name="artist_tags",
        ),
        migrations.RemoveField(
            model_name="artfile",
            name="content_tags",
        ),
        migrations.RemoveField(
            model_name="artfile",
            name="group_tags",
        ),
        migrations.DeleteModel(
            name="ArtistTag",
        ),
        migrations.DeleteModel(
            name="ContentTag",
        ),
        migrations.DeleteModel(
            name="GroupTag",
        ),
        migrations.AddConstraint(
            model_name="artfiletag",
            constraint=models.UniqueConstraint(
                fields=("name", "category"), name="unique_artfiletag_category_name"
            ),
        ),
        migrations.AddField(
            model_name="artfile",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="artfiles", to="textmode.artfiletag"
            ),
        ),
    ]
