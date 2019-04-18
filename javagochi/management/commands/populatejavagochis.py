from django.core.management.base import BaseCommand
from django.core.files import File
from javagochi.models import Javagochi, JavagochiBase
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
        parser.add_argument('-s', '--sprites', type=str, help='Define the sprites location', )

    def create_javagochi(self, df, index):
        nickname = df['Nickname'][index]
        race_name = df['Race'][index]
        owner_username = df['Owner'][index]
        health = df['Health'][index]
        hunger = df['Hunger'][index]
        cold = df['Cold'][index]
        hot = df['Hot'][index]
        age = df['Age'][index]
        lvl = df['Level'][index]
        exp = df['Exp'][index]

        self.stdout.write("Adding {} to database...".format(nickname))

        race = JavagochiBase.objects.filter(race=race_name).first()
        if(JavagochiBase.objects.filter(race=race_name).exists() == False):
            self.stderr.write("There is no '{}' race".format(race_name))
            return
        owner = CustomUser.objects.filter(username=owner_username).first()
        if(CustomUser.objects.filter(username=owner_username).exists() == False):
            self.stderr.write("There is no '{}' user".format(owner_username))
            return

        if(owner.level < race.min_user_level and owner.is_superuser == False):
            print("Cannot add {} to the database ({} has too low level and is not admin)".format(nickname, owner_username))
            return

        jc = Javagochi.objects.create(nickname= nickname,
                                      race= race,
                                      owner= owner,
                                      current_health=race.max_health,
                                      current_hunger=0,
                                      current_hot=0,
                                      current_cold=0,
                                      current_age=1,
                                      current_level= 1,
                                      current_experience=0)

        if health != '-' and health <= race.max_health:
            jc.current_health = health
        if hunger != '-' and hunger <= race.max_hunger:
            jc.current_hunger = hunger
        if cold != '-' and cold <= race.max_cold:
            jc.current_cold = cold
        if hot != '-' and hot <= race.max_hot:
            jc.current_hot = hot
        if age != '-' and age <= race.max_age:
            jc.age = age
        if lvl != '-' and lvl <= MAX_JAVAGOCHI_LEVEL:
            jc.current_level = lvl
        if exp != '-':
            jc.current_experience = exp
        jc.save()
        self.stdout.write("{} has been added to the database".format(nickname))

    def handle(self, *args, **options):
        if(options['file']):
            df = pd.read_excel(options['file'], sheet_name='Javagochis')
        else:
            df = pd.read_excel(file, sheet_name='Javagochis')

        for i in df.index:
            self.create_javagochi(df, i)
