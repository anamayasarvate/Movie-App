from django.contrib import admin
from .models import Favourite

# Favourite model is registered so that it can be controlled by admin  

admin.site.register(Favourite)
