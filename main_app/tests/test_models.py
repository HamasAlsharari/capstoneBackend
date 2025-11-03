from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import Expense, Category, PaymentMethod, Profile
from datetime import date
from decimal import Decimal

class ModelsTest(TestCase):
    def setUp(self):
        # Users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass456')

        # Profiles
        self.profile1 = Profile.objects.create(user=self.user1, full_name='John Doe', currency='USD', monthly_budget=Decimal('1000.00'), image_url='http://example.com/john.png')
        self.profile2 = Profile.objects.create(user=self.user2, full_name='Jane Smith', currency='EUR', monthly_budget=Decimal('1500.00'))

        # Categories
        self.cat_food = Category.objects.create(name='Food', icon='🍔', color='#f44336')
        self.cat_transport = Category.objects.create(name='Transport', icon='🚗', color='#2196f3')

        # Payment Methods
        self.pay_card = PaymentMethod.objects.create(name='Visa', type='Card', last_four='1234')
        self.pay_cash = PaymentMethod.objects.create(name='Cash', type='Cash', last_four='0000')

        # Expenses
        self.expense1 = Expense.objects.create(user=self.user1, title='Groceries', amount=Decimal('50.75'), date=date(2025, 1, 1), description='Weekly groceries')
        self.expense2 = Expense.objects.create(user=self.user1, title='Bus Ticket', amount=Decimal('2.50'), date=date(2025, 1, 2))
        self.expense3 = Expense.objects.create(user=self.user2, title='Lunch', amount=Decimal('12.00'), date=date(2025, 1, 3))

        # Relate categories to expenses
        self.expense1.categories.set([self.cat_food])
        self.expense2.categories.set([self.cat_transport])
        self.expense3.categories.set([self.cat_food, self.cat_transport])

        # Relate payment methods to expenses
        self.expense1.payment_methods.set([self.pay_card])
        self.expense2.payment_methods.set([self.pay_cash])
        self.expense3.payment_methods.set([self.pay_card, self.pay_cash])

    def test_user_str(self):
        self.assertEqual(str(self.user1), 'user1')
        self.assertEqual(str(self.user2), 'user2')

    def test_profile_str(self):
        self.assertEqual(str(self.profile1), 'John Doe')
        self.assertEqual(str(self.profile2), 'Jane Smith')

    def test_category_str(self):
        self.assertEqual(str(self.cat_food), 'Food')
        self.assertEqual(str(self.cat_transport), 'Transport')

    def test_paymentmethod_str(self):
        self.assertEqual(str(self.pay_card), 'Visa')
        self.assertEqual(str(self.pay_cash), 'Cash')

    def test_expense_str(self):
        self.assertEqual(str(self.expense1), 'Groceries - 50.75')
        self.assertEqual(str(self.expense2), 'Bus Ticket - 2.50')
        self.assertEqual(str(self.expense3), 'Lunch - 12.00')


    def test_expense_user_relationship(self):
        self.assertEqual(self.expense1.user, self.user1)
        self.assertEqual(self.expense3.user, self.user2)

    def test_expense_category_relationship(self):
        self.assertIn(self.cat_food, self.expense1.categories.all())
        self.assertIn(self.cat_transport, self.expense2.categories.all())
        self.assertIn(self.cat_food, self.expense3.categories.all())
        self.assertIn(self.cat_transport, self.expense3.categories.all())

    def test_expense_paymentmethod_relationship(self):
        self.assertIn(self.pay_card, self.expense1.payment_methods.all())
        self.assertIn(self.pay_cash, self.expense2.payment_methods.all())
        self.assertIn(self.pay_card, self.expense3.payment_methods.all())
        self.assertIn(self.pay_cash, self.expense3.payment_methods.all())

    def test_profile_user_relationship(self):
        self.assertEqual(self.profile1.user, self.user1)
        self.assertEqual(self.profile2.user, self.user2)

    
    def test_deleting_user_cascades_to_expenses_and_profile(self):
        self.user1.delete()
        self.assertEqual(Expense.objects.filter(user__username='user1').count(), 0)
        self.assertEqual(Profile.objects.filter(user__username='user1').count(), 0)

    def test_deleting_category_does_not_delete_expense(self):
        self.cat_food.delete()
        self.assertEqual(Expense.objects.filter(title='Groceries').count(), 1)
        self.assertEqual(Expense.objects.filter(title='Lunch').count(), 1)

    def test_deleting_paymentmethod_does_not_delete_expense(self):
        self.pay_card.delete()
        self.assertEqual(Expense.objects.filter(title='Groceries').count(), 1)
        self.assertEqual(Expense.objects.filter(title='Lunch').count(), 1)