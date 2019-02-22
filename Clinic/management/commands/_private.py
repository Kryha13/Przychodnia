from faker import Factory
import random
from Clinic.models import Doctors



def create_name():
    fake = Factory.create("pl_PL")
    name = fake.name()
    return name


def create_doctors():
    for i in range(0, 25):
        Doctors.objects.create(name=''.join(create_name()))

