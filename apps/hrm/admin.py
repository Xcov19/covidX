from django.contrib import admin

from apps.hrm import models


@admin.register(models.Hospital)
class HospitalAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StaffRegistry)
class StaffRegistryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PatientRegistry)
class PatientRegistryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DoctorRegistry)
class DoctorRegistryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Prescriptions)
class PrescriptionsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OtNotes)
class OtNotesAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Wards)
class WardsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Beds)
class BedsAdmin(admin.ModelAdmin):
    pass
