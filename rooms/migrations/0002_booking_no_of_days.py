# Generated by Django 4.2.1 on 2023-05-24 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='no_of_days',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
