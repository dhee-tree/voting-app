# Generated by Django 4.0.4 on 2022-05-12 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0008_teachers_points'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Teachers',
            new_name='Higher',
        ),
    ]