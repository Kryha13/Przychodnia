# Generated by Django 2.1.7 on 2019-02-22 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Clinic', '0002_auto_20190222_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctors',
            name='category',
        ),
    ]
