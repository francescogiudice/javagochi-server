from django.contrib import admin

from .models import BaseItem, OwnedItem

admin.site.register(BaseItem)
admin.site.register(OwnedItem)
