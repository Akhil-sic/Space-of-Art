# Generated by Django 3.0.3 on 2020-03-07 16:56

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20200306_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portf',
            name='phoneno',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
    ]
