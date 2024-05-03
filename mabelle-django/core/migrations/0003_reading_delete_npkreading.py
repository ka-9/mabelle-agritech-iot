# Generated by Django 5.0.3 on 2024-05-01 14:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_rename_npksensor_npkreading"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reading",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "nitrogen_level",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "phosphorus_level",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "potassium_level",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "temperature",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "humidity",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="NPKReading",
        ),
    ]