from faker import Factory
import random
from Clinic.models import Doctors, Rooms, Categories
import random


def create_name():
    fake = Factory.create("en_GB")
    name = fake.name()
    return name


def create_categories():
    fake = Factory.create("en_GB")
    for i in range(1, 10):
        Categories.objects.create(name=fake.job())


def create_doctors():
    room = random.sample(range(1, 15), 14)
    fake = Factory.create("en_GB")
    for i in range(1, len(room)):
        Doctors.objects.create(name=''.join(create_name()), room_id=room[i],
                               description=fake.paragraphs(nb=3, ext_word_list=None),
                               category=random.choice(Categories.objects.all()))


def create_rooms():
    room = random.sample(range(1, 25), 15)
    for i in range(1, len(room)):
        Rooms.objects.create(roomNumber=room[i])
