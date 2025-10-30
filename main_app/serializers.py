from rest_framework import serializers
from .models import Expense, Category, PaymentMethod

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    payment_methods = PaymentMethodSerializer(many=True, read_only=True)
    class Meta:
        model = Expense
        fields = '__all__'