# Generated by Django 5.1.1 on 2024-10-02 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mozz", "0005_rename_grid_columns_artpost_grid_column_span_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="artpost",
            name="grid_column_span",
        ),
        migrations.RemoveField(
            model_name="artpost",
            name="grid_row_span",
        ),
    ]
