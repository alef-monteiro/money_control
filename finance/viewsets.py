from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, status
from rest_framework import generics, permissions, response, serializers
from rest_framework.views import APIView
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
