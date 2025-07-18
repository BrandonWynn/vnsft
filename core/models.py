from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)  # E.g., FAAO_DETAIL, FAAO_BODY

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLES = [
        ('QC', 'Quality Control'),
        ('LEAD', 'Lead'),
        ('FOREMAN', 'Site Foreman'),
        ('REGIONAL', 'Regional'),
        ('ADMIN', 'Admin'),
        ('PRODUCTION', 'Production Manager'),
        ('SSD', 'SHINE Standards Director'),
        ('PROCESS', 'Body Shop Process'),
    ]
    role = models.CharField(max_length=20, choices=ROLES)
    assigned_locations = models.ManyToManyField(Location)
    manager_pin = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )  # ✅ For redo overrides; store hashed in prod

    def __str__(self):
        return f"{self.username} ({self.role})"


class Vehicle(models.Model):
    vin = models.CharField(max_length=17, unique=True)
    year = models.CharField(max_length=4, blank=True)
    make = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    account_name = models.CharField(max_length=100, blank=True)
    work_order = models.CharField(max_length=50, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Added for audit trail
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vin


class Service(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50)  # E.g., Full Detail, Redo, QC Check
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    started_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='services_started'
    )
    completed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='services_completed'
    )
    is_redo = models.BooleanField(default=False)
    manager_pin_used = models.BooleanField(default=False)
    sop_acknowledged = models.BooleanField(default=False)  # ✅ QC must acknowledge SOP before starting

    def __str__(self):
        return f"{self.service_type} for {self.vehicle.vin}"
