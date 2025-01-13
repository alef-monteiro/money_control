from django_filters import rest_framework as filters

from finance.models import CustomUser, Expenses, Cards, Categories


class CustomUserFilter(filters.FilterSet):
    """
    Filtros para o modelo CustomUser.
    """
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    balance = filters.NumberFilter(lookup_expr='gte')
    email = filters.CharFilter(lookup_expr='icontains')  # Filtra por email com busca parcial
    is_active = filters.BooleanFilter()  # Filtra por usuários ativos/inativos

    class Meta:
        model = CustomUser
        fields = '__all__'  # Campos disponíveis para filtragem


class ExpensesFilter(filters.FilterSet):
    user_name = filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    card_name = filters.CharFilter(field_name='card__name', lookup_expr='icontains')
    card_balance = filters.NumberFilter(field_name='card__balance', lookup_expr='gte')
    card_brand = filters.CharFilter(field_name='card__brand', lookup_expr='icontains')
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    amount = filters.NumberFilter(lookup_expr='gte')
    currency = filters.CharFilter(lookup_expr='icontains')
    payment_type = filters.CharFilter(lookup_expr='icontains')
    purchase_date = filters.DateFilter(lookup_expr='gte')
    due_date = filters.DateFilter(lookup_expr='lte')
    status = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Expenses
        fields = '__all__'


class CardsFilter(filters.FilterSet):
    user_name = filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    balance = filters.NumberFilter(lookup_expr='gte')
    card_brand = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Cards
        fields = '__all__'


class CategoriesFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Categories
        fields = '__all__'
