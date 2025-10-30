from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    categories = models.ManyToManyField('Category', related_name='expenses', blank=True)
    payment_methods = models.ManyToManyField('PaymentMethod', related_name="expenses", blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"

class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True, null=True) 
    color = models.CharField(max_length=20, default="#16a34a")

    def _str_(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    last_four = models.CharField(max_length=4)
