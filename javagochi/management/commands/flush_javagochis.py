from django.core.management.base import BaseCommand
from javagochi.models import JavagochiBase

class Command(BaseCommand):
    help = 'Deletes the database. USE WITH CARE'

    def handle(self, *args, **options):
        for javagochi in JavagochiBase.objects.all():
            javagochi.delete()
