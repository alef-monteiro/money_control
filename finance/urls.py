from django.urls import path, include
from rest_framework.routers import DefaultRouter
from finance import viewsets

router = DefaultRouter()
router.register('users', viewsets.CustomUserViewSet, basename='users')
router.register('expenses', viewsets.ExpensesViewSet, basename='expenses')
router.register('cards', viewsets.CardsViewSet, basename='cards')
router.register('categories', viewsets.CategoriesViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),  # Rotas do router
    path('token/', viewsets.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', viewsets.RegisterUserViewSet.as_view(), name='register'),
    path('login/', viewsets.LoginUserViewSet.as_view(), name='login'),
    path('logout/', viewsets.LogoutUserViewSet.as_view(), name='logout'),
    path('user/update/', viewsets.CustomUserUpdateAPIViewSet.as_view(), name='user_update'),
]
