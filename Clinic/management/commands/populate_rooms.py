from django.core.management.base import BaseCommand
from Clinic.management.commands._private import create_doctors, create_rooms


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_rooms()
        self.stdout.write(self.style.SUCCESS("Successfully created Rooms"))
