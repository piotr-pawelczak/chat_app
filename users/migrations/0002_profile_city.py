# Generated by Django 3.0.8 on 2022-05-27 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
