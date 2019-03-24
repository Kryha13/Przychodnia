from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
# Create your models here.


class Facility(models.Model):
    name = models.TextField(max_length=100)
    coordinates = models.PointField(help_text="To generate the map for your location")


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/media/', blank=True)

    def __str__(self):
        return str(self.user)



@receiver(post_save, sender=User)
def create_user_patient(sender, instance, created, **kwargs):
    if created:
        Patient.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_patient(sender, instance, **kwargs):
    instance.patient.save()


class Rooms(models.Model):
    roomNumber = models.SmallIntegerField(default=None)

    def __str__(self):
        return str(self.roomNumber)


class Categories(models.Model):
    name = models.TextField(max_length=100)

    def str(self):
        return self.name


class Doctors(models.Model):
    name = models.TextField(max_length=100)
    room = models.OneToOneField(Rooms, on_delete=models.PROTECT)
    description = models.TextField(default=None, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='static/media/', blank=True)

    def __str__(self):
        return self.name


class Accounts(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)


class Messages(models.Model):
    first_name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)
    email = models.EmailField(max_length=100)
    text = models.TextField()
    patient = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)


class Visits(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.TimeField()

    def __str__(self):
        return str('{} - {} - {}'.format(self.doctor, self.date, self.hour))


class Results(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit = models.ForeignKey(Visits, on_delete=models.CASCADE, default=None)
    paper = models.ImageField(upload_to='static/media/', blank=True)

