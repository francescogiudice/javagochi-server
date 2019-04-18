from django.core.management.base import BaseCommand
from django.core.files import File
from users.models import ExpMap
import pandas as pd
import os
from javagochi_server.settings import BASE_DIR

FILE_NAME = "Dbinfo.xlsx"

file = os.path.join(BASE_DIR, FILE_NAME)

class Command(BaseCommand):
    help = 'Loads the users in the database. The excel file and the image folder need to be located at the root directory. '\
           'If not you need to indicate the location with -f and -i respectively'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str, help='Define the excel file location', )
        parser.add_argument('-i', '--images', type=str, help='Define the image location', )

    def create_exp_map(self, df, index):
        level = df['Level'][index]
        exp_for_next_level = df['Exp needed'][index]
        coins_reward = df['Coins reward'][index]

        if(ExpMap.objects.filter(level=level).first()):
            return

        map = ExpMap(level=level, exp_for_next_level=exp_for_next_level, coins_reward=coins_reward)
        map.save()

        self.stdout.write("Map for level {} has been added to the database".format(level))

    def handle(self, *args, **options):
        if(options['file']):
            df = pd.read_excel(options['file'], sheet_name='User Exp Maps')
        else:
            df = pd.read_excel(file, sheet_name='User Exp Maps')

        for i in df.index:
            self.create_exp_map(df, i)
