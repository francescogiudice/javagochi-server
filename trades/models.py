from django.db import models
from javagochi.models import Javagochi, JavagochiBase

class TradeOffer(models.Model):
    offering = models.ForeignKey(Javagochi, on_delete=models.CASCADE, blank=False)
    interested_into = models.ForeignKey(JavagochiBase, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.offering.owner.username + " trading " + self.offering.race.race + " for " + self.interested_into.race
