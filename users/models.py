from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    level = models.IntegerField(default = 1)
    exp = models.IntegerField(default = 0)
    coins = models.IntegerField(default = 1000)
    image = models.ImageField(upload_to='profile_image', blank=True)

class ExpMap(models.Model):
    level = models.IntegerField(primary_key=True)
    exp_for_next_level = models.IntegerField()
    coins_reward = models.IntegerField()

    def __str__(self):
        return str(self.level) + " -> " + str(self.exp_for_next_level)
