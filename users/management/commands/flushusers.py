from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Deletes the users in the database. USE WITH CARE'

    def handle(self, *args, **options):
        for user in CustomUser.objects.all():
            user.delete()
