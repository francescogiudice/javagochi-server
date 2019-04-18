from django.core.management.base import BaseCommand
from django.core.files import File
from users.models import CustomUser
import pandas as pd
import os
from javagochi_server.settings import BASE_DIR

FILE_NAME = "Dbinfo.xlsx"
IMAGES_NAME_DIR = "user_images"

file = os.path.join(BASE_DIR, FILE_NAME)
images_dir = os.path.join(BASE_DIR, IMAGES_NAME_DIR)

class Command(BaseCommand):
    help = 'Loads the users in the database. The excel file and the image folder need to be located at the root directory. '\
           'If not you need to indicate the location with -f and -i respectively'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str, help='Define the excel file location', )
        parser.add_argument('-i', '--images', type=str, help='Define the image location', )

    def create_user(self, df, index, sprites):
        username = df['Username'][index]
        self.stdout.write("Adding {} to database...".format(username))
        password = df['Password'][index]
        email = df['Email'][index]
        coins = df['Coins'][index]
        lvl = df['Level'][index]
        exp = df['Exp'][index]

        if(CustomUser.objects.filter(username=username).first()):
            self.stdout.write("{} was already in database".format(username))
            return

        user = CustomUser.objects.create_user(username, password=password)
        user.email = email
        user.coins = coins
        user.level = lvl
        user.exp = exp

        img_path = os.path.join(sprites, username) + ".png"
        user.image.save(username + ".png", File(open(img_path, 'rb')))

        self.stdout.write("{} has been added to the database".format(username))

    def handle(self, *args, **options):
        if(options['file']):
            df = pd.read_excel(options['file'], sheet_name='Users')
        else:
            df = pd.read_excel(file, sheet_name='Users')

        if(options['images']):
            images = options['images']
        else:
            images = images_dir

        for i in df.index:
            self.create_user(df, i, images)
