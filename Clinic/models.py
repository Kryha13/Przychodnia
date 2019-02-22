from django.db import models

# Create your models here.


class Doctors(models.Model):
    name = models.TextField(max_length=30)
    surname = models.TextField(max_length=50)
    category = models.TextField(max_length=100)


class Rooms(models.Model):
    roomNumber = models.SmallIntegerField(default=None)
    doctor = models.OneToOneField(Doctors, on_delete=models.PROTECT)


class Categories(models.Model):
    name = models.TextField(max_length=100)
    doctor = models.OneToOneField(Doctors, on_delete=models.PROTECT)


class Patients(models.Model):
    name = models.TextField(max_length=30)
    surname = models.TextField(max_length=50)
    dateOfBirth = models.DateField(default=None)
    doctors = models.ManyToManyField(Doctors)


class Results(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    paper = models.ImageField()


