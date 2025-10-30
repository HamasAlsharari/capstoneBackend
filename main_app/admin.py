from django.contrib import admin
from .models import Expense, Category, PaymentMethod

admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(PaymentMethod)

