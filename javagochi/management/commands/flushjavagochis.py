from django.core.management.base import BaseCommand
from javagochi.models import Javagochi

class Command(BaseCommand):
    help = 'Deletes all the Javagochis in the database. USE WITH CARE'

    def handle(self, *args, **options):
        for javagochi in Javagochi.objects.all():
            javagochi.delete()
