# Generated by Django 3.1.4 on 2021-03-11 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characterBuilder', '0008_user_accepts_terms'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='arrow_count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='charactertest',
            name='question',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='charactertestchoice',
            name='choice',
            field=models.CharField(max_length=400),
        ),
    ]