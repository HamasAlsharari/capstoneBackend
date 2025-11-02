from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    Home, ExpenseListView, ExpenseDetailView,
    CategoryList, CategoryDetail, AddCategoryToExpense, RemoveCategoryFromExpense,
    PaymentMethodList, PaymentMethodDetail, AddPaymentMethodToExpense, RemovePaymentMethodFromExpense, ProfileDetail, update_profile,
    CreateUserView, LoginView, VerifyUserView
)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:category_id>/', CategoryDetail.as_view(), name='category-detail'),
    path('expenses/<int:expense_id>/add-category/<int:category_id>/', AddCategoryToExpense.as_view(), name='add-category'),
    path('expenses/<int:expense_id>/remove-category/<int:category_id>/', RemoveCategoryFromExpense.as_view(), name='remove-category'),
    path('payment-methods/', PaymentMethodList.as_view(), name='pm-list'),
    path('payment-methods/<int:pm_id>/', PaymentMethodDetail.as_view(), name='pm-detail'),
    path('expenses/<int:expense_id>/add-pm/<int:pm_id>/', AddPaymentMethodToExpense.as_view(), name='add-pm'),
    path('expenses/<int:expense_id>/remove-pm/<int:pm_id>/', RemovePaymentMethodFromExpense.as_view(), name='remove-pm'),
    path('users/<int:user_id>/add-profile/', ProfileDetail.as_view(), name='add-profile'),
    path('users/<int:user_id>/update-profile/', update_profile, name='update-profile'),
    path('users/signup/', CreateUserView.as_view(), name='signup'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/verify/', VerifyUserView.as_view(), name='verify-user'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]