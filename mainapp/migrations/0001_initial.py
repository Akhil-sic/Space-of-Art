# Generated by Django 3.0.3 on 2020-03-05 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('job_dec', models.CharField(max_length=200)),
                ('skills', models.TextField()),
                ('email', models.EmailField(max_length=100)),
                ('phoneno', models.IntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('address', models.TextField()),
                ('nationality', models.CharField(max_length=50)),
            ],
        ),
    ]
