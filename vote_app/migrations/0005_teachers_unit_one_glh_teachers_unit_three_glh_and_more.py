# Generated by Django 4.0.4 on 2022-04-23 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0004_teachers'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachers',
            name='unit_one_glh',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teachers',
            name='unit_three_glh',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='teachers',
            name='unit_two_glh',
            field=models.IntegerField(default=0),
        ),
    ]
