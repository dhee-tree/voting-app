# Generated by Django 4.0.4 on 2022-05-12 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0007_rename_higher_teachers'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachers',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
