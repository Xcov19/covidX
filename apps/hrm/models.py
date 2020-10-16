from covidx.common import utils
from django.db import models

MAX_LENGTH = 1000


class WorkerEnum(utils.EnumChoice):
    doctor = 1
    staff = 2


# Create your models here.
class Hospital(models.Model):
    name = models.CharField(blank=False, unique=True, max_length=MAX_LENGTH)
    address = models.TextField(
        blank=False,
    )
    city = models.CharField(blank=False, max_length=MAX_LENGTH)
    state = models.CharField(blank=False, max_length=MAX_LENGTH)
    country = models.CharField(blank=False, max_length=MAX_LENGTH)


class StaffRegistry(models.Model):
    hospital = models.ForeignKey(
        "Hospital", null=True, on_delete=models.deletion.SET_NULL
    )
    staff = models.ForeignKey("Staff", null=True, on_delete=models.deletion.SET_NULL)


class PatientRegistry(models.Model):
    pass


class DoctorRegistry(models.Model):
    hospital = models.ForeignKey(
        "Hospital", null=True, on_delete=models.deletion.SET_NULL
    )
    doctor = models.ForeignKey("Doctor", null=True, on_delete=models.deletion.SET_NULL)


class Doctor(models.Model):
    name = models.CharField(blank=False, max_length=MAX_LENGTH)
    designation = models.CharField(blank=False, max_length=MAX_LENGTH)
    attached_to = models.ManyToManyField(
        Hospital,
        through=DoctorRegistry,
    )


class Patient(models.Model):
    name = models.CharField(blank=False, max_length=MAX_LENGTH)
    age = models.IntegerField(
        blank=False,
    )
    admitted_in = models.ForeignKey(Hospital, on_delete=models.deletion.CASCADE)


class Staff(models.Model):
    name = models.CharField(blank=False, max_length=MAX_LENGTH)
    age = models.IntegerField(
        blank=False,
    )
    attached_to = models.ManyToManyField(
        Hospital,
        through=StaffRegistry,
    )
    designation = models.CharField(blank=False, max_length=MAX_LENGTH)


class Prescriptions(models.Model):
    for_patient = models.ForeignKey(Patient, on_delete=models.deletion.CASCADE)
    by_doctor = models.ForeignKey(Doctor, null=True, on_delete=models.deletion.SET_NULL)
    details = models.TextField(blank=False)


class OtNotes(models.Model):
    filled_by = models.CharField(choices=WorkerEnum.choices(), max_length=MAX_LENGTH)
    details = models.TextField(null=True)
    for_patient = models.ForeignKey(Patient, on_delete=models.deletion.CASCADE)


class Wards(models.Model):
    name = models.CharField(null=True, max_length=MAX_LENGTH)
    hospital = models.ForeignKey(Hospital, on_delete=models.deletion.CASCADE)


class Beds(models.Model):
    number = models.IntegerField()
    ward = models.ForeignKey(Wards, on_delete=models.deletion.CASCADE)
