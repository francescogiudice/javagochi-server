from django.db import models
from javagochi.models import Javagochi, JavagochiBase

class TradeOffer(models.Model):
    id = models.AutoField(primary_key=True)
    offering = models.ForeignKey(Javagochi, on_delete=models.CASCADE, blank=False)
    interested_into = models.ForeignKey(JavagochiBase, on_delete=models.CASCADE, blank=False)
    started = models.DateField(auto_now=True)

    def __str__(self):
        return self.offering.owner.username + " trading " + self.offering.race.race + " for " + self.interested_into.race
