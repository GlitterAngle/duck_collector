from django.contrib import admin

# Register your models here.
from .models import Duck, Feeding

admin.site.register(Duck)
admin.site.register(Feeding)