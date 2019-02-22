from django.core.management.base import BaseCommand
from Clinic.management.commands._private import create_doctors


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_doctors()
        self.stdout.write(self.style.SUCCESS("Successfully created Doctors"))

