from django.core.management.base import BaseCommand
from django.core.files import File
from items.models import BaseItem
import pandas as pd
import os
from javagochi_server.settings import BASE_DIR

FILE_NAME = "Dbinfo.xlsx"
SPRITES_NAME_DIR = "item_sprites"

file = os.path.join(BASE_DIR, FILE_NAME)
sprites_dir = os.path.join(BASE_DIR, SPRITES_NAME_DIR)

class Command(BaseCommand):
    help = 'Populates the database. The excel file and the sprites folder need to be located at the root directory. If not you need to indicate the location with -f and -s respectively'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str, help='Define the file location', )
        parser.add_argument('-s', '--sprites', type=str, help='Define the sprites location', )

    def retrieve_race_line(self, file, race):
        for i in file.index:
            if(file['Name'][i] == race):
                return i

    def create_item(self, df, index, sprites):
        name = df['Name'][index]
        property = df['Property'][index]
        amount = df['Amount'][index]
        coins = df['Cost'][index]
        buy_exp = df['Exp on buy'][index]
        usr_use_exp = df['Usr exp on use'][index]
        jc_use_exp = df['Jc exp on use'][index]

        self.stdout.write("Adding {} to database...".format(name))

        if(BaseItem.objects.filter(name=name).first()):
            self.stdout.write("{} was already in database".format(name))
            return

        item = BaseItem(name=name)
        item.property_modified = property
        item.amount_modified = amount
        item.cost = coins
        item.exp_on_buy = buy_exp
        item.user_exp_on_use = usr_use_exp
        item.jc_exp_on_use = jc_use_exp

        img_path = os.path.join(sprites, name) + ".png"
        item.image.save(name + ".png", File(open(img_path, 'rb')))

        item.save()
        self.stdout.write("{} has been added to the database".format(name))

    def handle(self, *args, **options):
        if(options['file']):
            df = pd.read_excel(options['file'], sheet_name='Base Items')
        else:
            df = pd.read_excel(file, sheet_name='Base Items')

        if(options['sprites']):
            sprites = options['sprites']
        else:
            sprites = sprites_dir

        for i in df.index:
            self.create_item(df, i, sprites)
