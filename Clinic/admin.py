from django.contrib import admin
from mapwidgets.widgets import GoogleStaticMapWidget, GoogleStaticOverlayMapWidget, GooglePointFieldWidget
from django.contrib.gis.db import models

# Register your models here.
from .models import Visits, Results, Patient, Doctors, Facility

admin.site.register(Visits)
admin.site.register(Results)
admin.site.register(Patient)
admin.site.register(Doctors)
admin.site.register(Facility)


class FacilityAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GoogleStaticMapWidget}
    }
