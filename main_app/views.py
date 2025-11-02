from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken 
from .models import Expense, Category, PaymentMethod, Profile
from .serializers import ExpenseSerializer, CategorySerializer, PaymentMethodSerializer, ProfileSerializer, UserSerializer
from django.contrib.auth import authenticate


class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the ExpenseTracker API!'}
        return Response(content)


class ExpenseListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get(self, request):
        try:
            expenses = Expense.objects.all()
            serializer = self.serializer_class(expenses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        data = request.data.copy()
        data["user"] = int(request.user.id)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, expense_id, category_id):
        expense = get_object_or_404(Expense, id=expense_id)
        category = get_object_or_404(Category, id=category_id)
        expense.categories.add(category)
        serializer = CategorySerializer(expense.categories.all(), many=True)
        return Response({"categories": serializer.data}, status=status.HTTP_200_OK)

class RemoveCategoryFromExpense(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, expense_id, category_id):
        expense = get_object_or_404(Expense, id=expense_id)
        category = get_object_or_404(Category, id=category_id)
        expense.categories.remove(category)
        serializer = CategorySerializer(expense.categories.all(), many=True)
        return Response({"categories": serializer.data}, status=status.HTTP_200_OK)

class PaymentMethodList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentMethodSerializer
    queryset = PaymentMethod.objects.all()

class PaymentMethodDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, expense_id, pm_id):
        expense = get_object_or_404(Expense, id=expense_id)
        pm = get_object_or_404(PaymentMethod, id=pm_id)
        expense.payment_methods.add(pm)
        return Response({'success': True})

class RemovePaymentMethodFromExpense(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, expense_id, pm_id):
        expense = get_object_or_404(Expense, id=expense_id)
        pm = get_object_or_404(PaymentMethod, id=pm_id)
        expense.payment_methods.remove(pm)
        return Response({'success': True})

class ProfileDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def post(self, request, user_id):
        data = request.data.copy()
        data["user"] = int(user_id)

        existing_profile = Profile.objects.filter(user=user_id)
        if existing_profile.exists():
            existing_profile.delete()

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            user = get_object_or_404(User, id=user_id)
            serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_profile(request, user_id):
    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        user = get_object_or_404(User, id=user_id)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    try:
      user = User.objects.get(username=request.user.username)
      try:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),'access': str(refresh.access_token),'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
      except Exception as token_error:
        return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
      return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)