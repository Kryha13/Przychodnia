# Generated by Django 2.1.7 on 2019-03-13 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clinic', '0007_auto_20190313_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/media/'),
        ),
    ]
