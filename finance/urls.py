from django.urls import path, include
from rest_framework.routers import DefaultRouter
from finance import viewsets

router = DefaultRouter()
router.register('users', viewsets.CustomUserViewSet, basename='users')
router.register('expenses', viewsets.ExpensesViewSet, basename='expenses')
router.register('cards', viewsets.CardsViewSet, basename='cards')
router.register('categories', viewsets.CategoriesViewSet, basename='categories')

urlpatterns = [
    # Incluindo as rotas do router
    path('', include(router.urls)),

    # Endpoints personalizados
    path('token/', viewsets.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', viewsets.RegisterUserViewSet.as_view(), name='register'),  # Registro de usuário
    path('login/', viewsets.LoginUserViewSet.as_view(), name='login'),  # Login de usuário
    path('logout/', viewsets.LogoutUserViewSet.as_view(), name='logout'),  # Logout de usuário

    # Atualização de dados do usuário autenticado
    path('user/update/', viewsets.CustomUserUpdateAPIViewSet.as_view(), name='user_update'),
]
