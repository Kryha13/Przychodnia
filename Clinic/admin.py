from django.contrib import admin

# Register your models here.
from .models import Visits, Results, Patient

admin.site.register(Visits)
admin.site.register(Results)
admin.site.register(Patient)