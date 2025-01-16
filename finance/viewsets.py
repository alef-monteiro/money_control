from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, status
from rest_framework import generics, permissions, response, serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from finance import serializers, models, filters

User = get_user_model()

class CustomTokenObtainPairView(APIView):
    """
    Custom token obtain view for JWT with email-based authentication.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return response.Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return response.Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)

        return response.Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )

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

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return response.Response({'message': 'Usuário excluído com sucesso'}, status=status.HTTP_200_OK)

class LoginUserViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                # Gerar token JWT
                refresh = RefreshToken.for_user(user)
                return response.Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)
            return response.Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return response.Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutUserViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return response.Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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