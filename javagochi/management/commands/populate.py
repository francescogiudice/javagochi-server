from django.core.management.base import BaseCommand
from django.core.files import File
from javagochi.models import JavagochiBase
import pandas as pd
import os

file = ("C:\\Users\\Manu\\Downloads\\Javagochi classes.xlsx")
sprites_dir = ("C:\\Users\\Manu\\Downloads\\Sprites")

# At index 0 there is a table that indicates the stats of the Javagochis in this order:
# -1: Name
# -2: Health
# -3: Hunger
# -4: Cold
# -5: Hot
# -6: Age
# -7: Evolves at
# -8: Evolves into
# -9: Coins needed
# -10: Min. user level

class Command(BaseCommand):
    help = 'Populates the database'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str, help='Define the file location', )
        parser.add_argument('-s', '--sprites', type=str, help='Define the sprites location', )

    # def _excel_to_dict(self, file, index):
    #     dict = {
    #         "name" = df['Name'][index],
    #         "health" = df['Health'][index],
    #         "hunger" = df['Hunger'][index],
    #         "cold" = df['Cold'][index],
    #         "hot" = df['Hot'][index],
    #         "age" = df['Age'][index],
    #         "evolves_at" = df['Evolves at'][index],
    #         "evolves_into" = df['Evolves Into'][index],
    #         "coins" = df['Coins needed'][index],
    #         "usr_lvl" = df['Min level'][index]
    #     }
    #
    #     return dict

    def retrieve_race_line(self, file, race):
        for i in file.index:
            if(file['Name'][i] == race):
                return i

    def create_javagochi(self, df, index, sprites):
        name = df['Name'][index]
        print("Adding {}".format(name))
        health = df['Health'][index]
        hunger = df['Hunger'][index]
        cold = df['Cold'][index]
        hot = df['Hot'][index]
        age = df['Age'][index]
        evolves_at = df['Evolves at'][index]
        evolves_into = df['Evolves into'][index]
        coins = df['Coins needed'][index]
        usr_lvl = df['Min level'][index]
        exp = df['Exp'][index]

        if(JavagochiBase.objects.filter(race=name).first()):
            print("Already in database")
            return

        jc = JavagochiBase(race=name)
        jc.max_health = health
        jc.max_hunger = hunger
        jc.max_cold = cold
        jc.max_hot = hot
        jc.max_age = age
        jc.cost = coins
        jc.min_user_level = usr_lvl
        jc.exp_on_buy = exp

        img_path = os.path.join(sprites, name) + ".gif"
        jc.image.save(name + ".gif", File(open(img_path, 'rb')))

        if(df['Evolves into'][index] != '-' and df['Evolves into'][index] != ''):
            evolution = JavagochiBase.objects.filter(race=evolves_into).first()
            if(JavagochiBase.objects.filter(race=evolves_into).count() == 0):
                index = self.retrieve_race_line(df, evolves_into)
                self.create_javagochi(df, index, sprites)
                evolution = JavagochiBase.objects.filter(race=evolves_into).first()
            jc.evolves_at = evolves_at
            jc.evolves_into = evolution
        jc.save()

    def handle(self, *args, **options):
        if(options['file']):
            df = pd.read_excel(options['file'], sheet_name='Classes')
        else:
            df = pd.read_excel(file, sheet_name='Classes')

        if(options['sprites']):
            sprites = options['sprites']
        else:
            sprites = sprites_dir

        for i in df.index:
            self.create_javagochi(df, i, sprites)
