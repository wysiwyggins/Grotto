# Generated by Django 3.1.4 on 2021-03-11 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapBuilder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='arrow_count',
            field=models.IntegerField(default=0),
        ),
    ]