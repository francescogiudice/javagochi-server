from django.contrib import admin
from .models import Javagochi, JavagochiBase, JavagochiExpMap, JavagochiType

admin.site.register(Javagochi)
admin.site.register(JavagochiBase)
admin.site.register(JavagochiExpMap)
admin.site.register(JavagochiType)
