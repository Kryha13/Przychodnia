from django.db import models
from .forms import UserForm
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_patient(sender, instance, created, **kwargs):
    if created:
        Patient.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_patient(sender, instance, **kwargs):
    instance.patient.save()


class Doctors(models.Model):
    name = models.TextField(max_length=100)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True)


class Rooms(models.Model):
    roomNumber = models.SmallIntegerField(default=None)
    doctor = models.OneToOneField(Doctors, on_delete=models.PROTECT)


class Categories(models.Model):
    name = models.TextField(max_length=100)
    doctor = models.OneToOneField(Doctors, on_delete=models.PROTECT)


class Results(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    paper = models.ImageField()


class Accounts(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)


class Messages(models.Model):
    first_name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)
    email = models.EmailField(max_length=100)
    text = models.TextField()
    patient = models.ForeignKey(User, null=True, on_delete=models.PROTECT)