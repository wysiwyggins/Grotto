# Generated by Django 3.1.4 on 2021-02-24 03:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mapBuilder", "0001_initial"),
        ("characterBuilder", "0006_auto_20210223_1912"),
    ]

    operations = [
        migrations.AlterField(
            model_name="character",
            name="room",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="occupants",
                to="mapBuilder.room",
            ),
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "character",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="characterBuilder.character",
                    ),
                ),
            ],
        ),
    ]
