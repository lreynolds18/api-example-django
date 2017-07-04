from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Docter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = PhoneNumberField()
    doctor = models.ForeignKey(Docter, on_delete=models.CASCADE)
