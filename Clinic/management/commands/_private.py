from faker import Factory
import random
from Clinic.models import Doctors, Rooms
import random


def create_name():
    fake = Factory.create("pl_PL")
    name = fake.name()
    return name


def create_doctors():
    room = random.sample(range(1, 15), 14)
    for i in range(1, len(room)):
        Doctors.objects.create(name=''.join(create_name()), room_id=room[i])


def create_rooms():
    room = random.sample(range(1, 25), 15)
    for i in range(1, len(room)):
        Rooms.objects.create(roomNumber=room[i])
