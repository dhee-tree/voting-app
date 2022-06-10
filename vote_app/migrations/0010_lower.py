# Generated by Django 4.0.4 on 2022-05-25 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0009_rename_teachers_higher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unit_one', models.CharField(max_length=100)),
                ('unit_one_glh', models.IntegerField(default=0)),
                ('unit_two', models.CharField(max_length=100)),
                ('unit_two_glh', models.IntegerField(default=0)),
                ('unit_three', models.CharField(max_length=100)),
                ('unit_three_glh', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
            ],
        ),
    ]