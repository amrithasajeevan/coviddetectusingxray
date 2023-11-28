

# Register your models here.
from django.contrib import admin

from cpapp import models

admin.site.register(models.Login)
admin.site.register(models.PatientLogin)
admin.site.register(models.DoctorLogin)
admin.site.register(models.PharmacyLogin)
admin.site.register(models.Prescription)
admin.site.register(models.buy_medicines)

