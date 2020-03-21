from django.contrib import admin
from .models import Finch, Sighting, Armor, Photo
# Register your models here.

admin.site.register(Finch)
admin.site.register(Sighting)
admin.site.register(Armor)
admin.site.register(Photo)
