# Generated by Django 4.0.4 on 2022-04-20 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0002_uservote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservote',
            name='email',
            field=models.EmailField(max_length=250),
        ),
    ]
