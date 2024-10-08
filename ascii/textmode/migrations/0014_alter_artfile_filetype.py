# Generated by Django 4.2.11 on 2024-09-04 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("textmode", "0013_artfile_aspect_ratio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artfile",
            name="filetype",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "None"),
                    (1, "ASCII"),
                    (2, "ANSi"),
                    (3, "ANSiMation"),
                    (4, "RIP script"),
                    (5, "PCBoard"),
                    (6, "Avatar"),
                    (7, "HTML"),
                    (8, "Source"),
                    (9, "TundraDraw"),
                    (10, "GIF"),
                    (11, "PCX"),
                    (12, "LBM/IFF"),
                    (13, "TGA"),
                    (14, "FLI"),
                    (15, "FLC"),
                    (16, "BMP"),
                    (17, "GL"),
                    (18, "DL"),
                    (19, "WPG Bitmap"),
                    (20, "PNG"),
                    (21, "JPG/JPeg"),
                    (22, "MPG"),
                    (23, "AVI"),
                    (24, "DXF"),
                    (25, "DWG"),
                    (26, "WPG Vector"),
                    (27, "3DS"),
                    (28, "MOD"),
                    (29, "669"),
                    (30, "STM"),
                    (31, "S3M"),
                    (32, "MTM"),
                    (33, "FAR"),
                    (34, "ULT"),
                    (35, "AMF"),
                    (36, "DMF"),
                    (37, "OKT"),
                    (38, "ROL"),
                    (39, "CMF"),
                    (40, "MID"),
                    (41, "SADT"),
                    (42, "VOC"),
                    (43, "WAV"),
                    (44, "SMP8"),
                    (45, "SMP8S"),
                    (46, "SMP16"),
                    (47, "SMP16S"),
                    (48, "PATCH8"),
                    (49, "PATCH16"),
                    (50, "XM"),
                    (51, "HSC"),
                    (52, "IT"),
                    (53, "binary"),
                    (54, "XBin"),
                    (55, "ZIP"),
                    (56, "ARJ"),
                    (57, "LZH"),
                    (58, "ARC"),
                    (59, "TAR"),
                    (60, "ZOO"),
                    (61, "RAR"),
                    (62, "UC2"),
                    (63, "PAK"),
                    (64, "SQZ"),
                    (65, "executable"),
                ],
                db_index=True,
                null=True,
            ),
        ),
    ]
