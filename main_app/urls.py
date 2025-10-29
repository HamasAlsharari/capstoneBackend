from django.urls import path
from .views import Home, ExpenseListView, ExpenseDetailView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('expenses/', ExpenseListView.as_view(), name='expenses-list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'), 
]