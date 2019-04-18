from django.core.management.base import BaseCommand
from django.core.files import File
from items.models import OwnedItem, BaseItem
from users.models import CustomUser
import pandas as pd
import os
from javagochi_server.settings import BASE_DIR
from consts import MAX_JAVAGOCHI_LEVEL

FILE_NAME = "Dbinfo.xlsx"

file = os.path.join(BASE_DIR, FILE_NAME)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str, help='Define the file location', )

    def create_item(self, df, index):
        item_type = df['Item'][index]
        owner_username = df['Owner'][index]
        amount = df['Amount owned'][index]

        self.stdout.write("Adding {} {} to {}...".format(amount, item_type, owner_username))

        base_item = BaseItem.objects.filter(name=item_type)
        if(base_item.exists() == False):
            self.stderr.write("There is no '{}' item".format(item_type))
            return
        owner = CustomUser.objects.filter(username=owner_username)
        if(owner.exists() == False):
            self.stderr.write("There is no '{}' user".format(owner_username))
            return

        if(OwnedItem.objects.filter(owner__username=owner_username, item__name=item_type).exists() == True):
            item = OwnedItem.objects.filter(owner__username=owner_username, item__name=item_type).first()
            item.amount_owned += amount
            item.save()
        else:
            item = OwnedItem.objects.create(item=base_item.first(), owner=owner.first(), amount_owned=amount)

        self.stdout.write("{} has been added to the database".format(item_type))

    def handle(self, *args, **options):
        if(options['file']):
            df = pd.read_excel(options['file'], sheet_name='Owned Items')
        else:
            df = pd.read_excel(file, sheet_name='Owned Items')

        for i in df.index:
            self.create_item(df, i)
