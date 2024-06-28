from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('EMPLOYEE', 'Employee'),
        ('MANAGER', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    items_ordered = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
