from django.contrib import admin

# Register your models here.

from store.models import *

admin.site.register(Productmodel)
admin.site.register(Categorymodel)
