# Generated by Django 2.1.7 on 2019-03-10 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Clinic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visits',
            name='room',
        ),
        migrations.AlterField(
            model_name='doctors',
            name='room',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='Clinic.Rooms'),
        ),
    ]
