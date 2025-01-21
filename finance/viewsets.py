# Imports do Django
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Sum
from django.db.models.functions import TruncMonth

# Imports do DRF (Django Rest Framework)
from rest_framework import (
    viewsets,
    status,
    generics,
    permissions,
    response,
    serializers,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Imports do DRF Simple JWT
from rest_framework_simplejwt import views
from rest_framework_simplejwt.tokens import RefreshToken

from finance import serializers, models, filters

User = get_user_model()


# Fiz mudanças para resolver o problemas de payload

class CustomTokenObtainPairView(views.TokenObtainPairView):
    """
    Custom token obtain view for JWT with email-based authentication.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CustomTokenObtainPairSerializer


class RegisterUserViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return response.Response(
                {
                    'message': 'Usuário criado com sucesso',
                    'user': serializer.data
                },
                status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserUpdateAPIViewSet(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    # adicionado do codigo alex
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return response.Response({'message': 'Usuário excluído com sucesso'},
                                 status=status.HTTP_200_OK)


class LoginUserViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)
            if user:
                # Gerar token JWT
                refresh = RefreshToken.for_user(user)
                return response.Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'message': 'Login com sucesso'
                }, status=status.HTTP_200_OK)
            return response.Response({'error': 'Credenciais inválidas'},
                                     status=status.HTTP_401_UNAUTHORIZED)
        return response.Response({'error': 'Email e senha obrigatórios'},
                                 status=status.HTTP_400_BAD_REQUEST)


class LogoutUserViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Deleta o token associado ao usuário
        return response.Response({'message': 'Logout com sucesso'}, status=status.HTTP_200_OK)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer
    filterset_class = filters.CustomUserFilter


class CardsViewSet(viewsets.ModelViewSet):
    queryset = models.Cards.objects.all()
    serializer_class = serializers.CardSerializer
    filters_class = filters.CardsFilter


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = models.Categories.objects.all()
    serializer_class = serializers.CategorySerializer
    filterset_class = filters.CategoriesFilter


class ExpensesViewSet(viewsets.ModelViewSet):
    queryset = models.Expenses.objects.all()
    serializer_class = serializers.ExpenseSerializer
    filterset_class = filters.ExpensesFilter

    def perform_create(self, serializer):
        card = serializer.validated_data['card']
        amount = serializer.validated_data['amount']
        if serializer.validated_data['payment_type'] == 'saída' and card.balance < amount:
            raise serializers.ValidationError({'detail': 'Saldo insuficiente no cartão.'})
        serializer.save(user=self.request.user)


# Dashboards Implementações
class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def total_balance(self, request):
        user = request.user
        total_balance = models.Cards.objects.filter(user=user).aggregate(Sum('balance'))['balance__sum'] or 0
        if total_balance is None:
            return Response({'error': 'Nenhum saldo encontrado'} or 0, status=404)
        return Response({'total_balance': total_balance})

    @action(detail=True, methods=['get'])
    def card_statement(self, request, pk=None):
        card = models.Cards.objects.filter(user=request.user, id=pk).first()
        if not card:
            return Response({'error': f'Cartão com ID {pk} não encontrado'}, status=404)
        serializer = serializers.CardStatementSerializer(card)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_expenses(self, request):
        expenses = models.Expenses.objects.filter(user=request.user)
        serializer = serializers.ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        user = request.user
        monthly_data = (
            models.Expenses.objects.filter(user=user)
            .annotate(month=TruncMonth('purchase_date'))
            .values('month')
            .annotate(
                total_in=Sum('amount', filter=models.Q(payment_type='entrada')),
                total_out=Sum('amount', filter=models.Q(payment_type='saída')),
            )
            .order_by('month')
        )
        serializer = serializers.MonthlySummarySerializer(monthly_data, many=True)
        return Response(serializer.data)
