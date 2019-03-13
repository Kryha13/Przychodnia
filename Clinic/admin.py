from django.contrib import admin

# Register your models here.
from .models import Visits, Results

admin.site.register(Visits)
admin.site.register(Results)