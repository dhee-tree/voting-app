# Generated by Django 4.0.4 on 2022-06-11 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0010_lower'),
    ]

    operations = [
        migrations.AddField(
            model_name='higher',
            name='unit_five',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='higher',
            name='unit_five_glh',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='higher',
            name='unit_four',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='higher',
            name='unit_four_glh',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lower',
            name='unit_five',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='lower',
            name='unit_five_glh',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lower',
            name='unit_four',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='lower',
            name='unit_four_glh',
            field=models.IntegerField(default=0),
        ),
    ]