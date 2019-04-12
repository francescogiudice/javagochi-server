from django.db import models
from users.models import CustomUser

class BaseItem(models.Model):
    image = models.ImageField(upload_to='items/')
    name = models.CharField(max_length = 256, primary_key = True)
    property_modified = models.CharField(max_length = 256)
    amount_modified = models.IntegerField()
    cost = models.IntegerField()
    exp_on_buy = models.IntegerField()
    user_exp_on_use = models.IntegerField()
    jc_exp_on_use = models.IntegerField()

    def __str__(self):
        return self.name

class OwnedItem(models.Model):
    item = models.ForeignKey(BaseItem, on_delete = models.CASCADE, blank=False)
    owner = models.ForeignKey(CustomUser, on_delete = models.CASCADE, blank=False)

    amount_owned = models.IntegerField()

    def __str__(self):
        return self.item.name + " of " + self.owner.username
