# Generated by Django 3.1.4 on 2022-01-08 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characterBuilder', '0016_auto_20211211_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='arrow_count',
        ),
    ]
