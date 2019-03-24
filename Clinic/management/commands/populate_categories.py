from django.core.management.base import BaseCommand
from Clinic.management.commands._private import create_categories


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_categories()
        self.stdout.write(self.style.SUCCESS("Successfully created Categories"))
