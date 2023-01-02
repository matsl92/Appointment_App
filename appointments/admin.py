from django.contrib import admin
from .models import Week, Gap, Appointment

admin.site.register([Week, Gap, Appointment])