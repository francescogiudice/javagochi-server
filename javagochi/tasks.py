from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from javagochi.models import Javagochi
from javagochi.scripts import take_damage

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="update_javagochis",
    ignore_resutl=True
)
def update_javagochis():
    logger.info("Starting Javagochis update...")

    for javagochi in Javagochi.objects.filter(owner__is_superuser=False):
        logger.info("Updating " + javagochi.nickname)

        # Increase hunger
        javagochi.current_hunger = min(javagochi.current_hunger + 10, javagochi.race.max_hunger)
        if(javagochi.current_hunger >= javagochi.race.max_hunger):
            take_damage(javagochi, 10)  # TODO make this parametric
            if(javagochi.current_health <= 0):
                return

        # Increase hot
        javagochi.current_hot = min(javagochi.current_hot + 10, javagochi.race.max_hot)
        if(javagochi.current_hot >= javagochi.race.max_hot):
            take_damage(javagochi, 10)  # TODO make this parametric
            if(javagochi.current_health <= 0):
                return

        # Increase cold
        javagochi.current_cold = min(javagochi.current_cold + 10, javagochi.race.max_cold)
        if(javagochi.current_cold >= javagochi.race.max_cold):
            take_damage(javagochi, 10)  # TODO make this parametric
            if(javagochi.current_health <= 0):
                return

        # Increase age
        javagochi.current_age += 1
        if(javagochi.current_age >= javagochi.race.max_age):
            javagochi.delete()
