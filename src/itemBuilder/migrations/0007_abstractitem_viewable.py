# Generated by Django 3.1.4 on 2022-01-08 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemBuilder', '0006_swap'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractitem',
            name='viewable',
            field=models.BooleanField(default=False),
        ),
    ]
