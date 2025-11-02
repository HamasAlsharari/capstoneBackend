from django.contrib import admin
from .models import Expense, Category, PaymentMethod, Profile

admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(PaymentMethod)
admin.site.register(Profile)

