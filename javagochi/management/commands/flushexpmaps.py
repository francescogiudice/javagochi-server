from django.core.management.base import BaseCommand
from javagochi.models import JavagochiExpMap

class Command(BaseCommand):
    help = 'Deletes all the Javagochi Exp Map in the database. USE WITH CARE'

    def handle(self, *args, **options):
        for map in JavagochiExpMap.objects.all():
            map.delete()
