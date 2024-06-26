# Generated by Django 4.2.11 on 2024-04-25 01:18

import ascii.core.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("translations", "0002_alter_translation_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="translation",
            name="original",
            field=ascii.core.fields.NonStrippingTextField(db_index=True),
        ),
        migrations.AlterField(
            model_name="translation",
            name="translated",
            field=ascii.core.fields.NonStrippingTextField(blank=True),
        ),
    ]
