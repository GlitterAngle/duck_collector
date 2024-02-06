from django.contrib import admin

# Register your models here.
from .models import Duck, Feeding, Feather

admin.site.register(Duck)
admin.site.register(Feeding)
admin.site.register(Feather)