from datetime import timedelta
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from javagochi.models import Javagochi
from javagochi.scripts import take_damage
from consts import KILL_ALL

from datetime import date, datetime
from consts import HOT_N_COLD_PER_SEASON

Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
seasons = [('winter', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('spring', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('summer', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('autumn', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('winter', (date(Y, 12, 21),  date(Y, 12, 31)))]

def get_season(now):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)

def get_hot_n_cold_increase():
    season = get_season(date.today())
    return HOT_N_COLD_PER_SEASON[season]

logger = get_task_logger(__name__)

@periodic_task(
    run_every=timedelta(seconds=10),
    name="update_javagochis",
    ignore_result=True
)
def update_javagochis():
    print("Starting server update")
    logger.info("Starting Javagochis update...")

    javagochis = Javagochi.objects.filter(owner__is_superuser=False)
    if(KILL_ALL):
        logger.info("Updating every javagochi")
        javagochis = Javagochi.objects.all()
    else:
        logger.info("Updating non superuser")

    for javagochi in javagochis:
        logger.info("Updating " + javagochi.nickname)

        # Increase hunger
        javagochi.current_hunger = min(javagochi.current_hunger + 10, javagochi.race.max_hunger)
        if(javagochi.current_hunger >= javagochi.race.max_hunger):
            take_damage(javagochi, 10)  # TODO make this parametric
            if(javagochi.current_health <= 0):
                return

        # Retrieve amount of hot and cold to increase. Information is stored in a dictionary
        hot_n_cold_dict = get_hot_n_cold_increase()
        hot = hot_n_cold_dict['hot']
        cold = hot_n_cold_dict['cold']

        # Increase hot
        javagochi.current_hot = min(javagochi.current_hot + hot, javagochi.race.max_hot)
        javagochi.current_hot = max(javagochi.current_hot, 0) # Prevents negative values
        if(javagochi.current_hot >= javagochi.race.max_hot):
            take_damage(javagochi, 10)  # TODO make this parametric
            if(javagochi.current_health <= 0):
                return

        # Increase cold
        javagochi.current_cold = min(javagochi.current_cold + cold, javagochi.race.max_cold)
        javagochi.current_cold = max(javagochi.current_cold, 0) # Prevents negative values
        if(javagochi.current_cold >= javagochi.race.max_cold):
            take_damage(javagochi, 10)  # TODO make this parametric
            if(javagochi.current_health <= 0):
                return

        # Increase age
        javagochi.current_age += 1
        if(javagochi.current_age >= javagochi.race.max_age):
            javagochi.delete()
            return

        javagochi.save()
