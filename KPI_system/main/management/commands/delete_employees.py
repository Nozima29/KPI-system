from django.core.management.base import BaseCommand, CommandError
from main.models import Employees


class Command(BaseCommand):
    def handle(self, *args, **options):
        Employees.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all employees'))