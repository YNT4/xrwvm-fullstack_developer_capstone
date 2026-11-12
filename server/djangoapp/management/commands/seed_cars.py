
from django.core.management.base import BaseCommand
from djangoapp.populate import initiate


class Command(BaseCommand):
    help = "Initialize car makes and models from sample data"

    def handle(self, *args, **options):
        initiate()
        self.stdout.write(
            self.style.SUCCESS("Car data seeding completed.")
        )
