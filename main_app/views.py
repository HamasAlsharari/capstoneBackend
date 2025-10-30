from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from .models import Expense, Category, PaymentMethod
from .serializers import ExpenseSerializer, CategorySerializer, PaymentMethodSerializer


class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the ExpenseTracker API!'}
        return Response(content)


class ExpenseListView(APIView):
    serializer_class = ExpenseSerializer

    def get(self, request):
        try:
            expenses = Expense.objects.all()
            serializer = self.serializer_class(expenses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailView(APIView):
    serializer_class = ExpenseSerializer
    lookup_field = 'pk'

    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            return None

    def get(self, request, pk):
        expense = self.get_object(pk)
        if expense is None:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        expense = self.get_object(pk)
        if expense is None:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense = self.get_object(pk)
        if expense is None:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(APIView):
    serializer_class = CategorySerializer
    lookup_field = 'category_id'

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        serializer = self.serializer_class(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        serializer = self.serializer_class(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)

class AddCategoryToExpense(APIView):
    def post(self, request, expense_id, category_id):
        expense = get_object_or_404(Expense, id=expense_id)
        category = get_object_or_404(Category, id=category_id)
        expense.categories.add(category)
        serializer = CategorySerializer(expense.categories.all(), many=True)
        return Response({"categories": serializer.data}, status=status.HTTP_200_OK)

class RemoveCategoryFromExpense(APIView):
    def post(self, request, expense_id, category_id):
        expense = get_object_or_404(Expense, id=expense_id)
        category = get_object_or_404(Category, id=category_id)
        expense.categories.remove(category)
        serializer = CategorySerializer(expense.categories.all(), many=True)
        return Response({"categories": serializer.data}, status=status.HTTP_200_OK)

class PaymentMethodList(generics.ListCreateAPIView):
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()

class PaymentMethodDetail(APIView):
    serializer_class = PaymentMethodSerializer

    def get(self, request, pm_id):
        pm = get_object_or_404(PaymentMethod, id=pm_id)
        return Response(self.serializer_class(pm).data)

    def put(self, request, pm_id):
        pm = get_object_or_404(PaymentMethod, id=pm_id)
        serializer = self.serializer_class(pm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pm_id):
        pm = get_object_or_404(PaymentMethod, id=pm_id)
        pm.delete()
        return Response({'success': True})
        
class AddPaymentMethodToExpense(APIView):
    def post(self, request, expense_id, pm_id):
        expense = get_object_or_404(Expense, id=expense_id)
        pm = get_object_or_404(PaymentMethod, id=pm_id)
        expense.payment_methods.add(pm)
        return Response({'success': True})

class RemovePaymentMethodFromExpense(APIView):
    def post(self, request, expense_id, pm_id):
        expense = get_object_or_404(Expense, id=expense_id)
        pm = get_object_or_404(PaymentMethod, id=pm_id)
        expense.payment_methods.remove(pm)
        return Response({'success': True})
