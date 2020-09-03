# Generated by Django 3.1 on 2020-09-03 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=20)),
            ],
        ),
    ]
