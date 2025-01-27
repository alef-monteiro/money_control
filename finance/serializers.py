from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from finance import models


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializador para retornar informações do usuário.
    """

    class Meta:
        model = models.CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def create(self, validated_data):
            # Criação de usuário com senha criptografada
            user = models.CustomUser.objects.create_user(validated_data)
            return user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Criação de usuário com senha criptografada
        user = models.CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)

        # Adicione os campos necessários ao payload
        token['id'] = user.id
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categories
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expenses
        fields = ['id', 'user', 'card', 'description', 'amount', 'purchase_date', 'payment_type']

    def validate(self, data):
        if data['payment_type'] == 'saída' and data['amount'] > data['card'].balance:
            raise serializers.ValidationError('Saldo insuficiente no cartão para esta despesa.')
        return data


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cards
        fields = '__all__'


# Dashboard implementações
class CardStatementSerializer(serializers.ModelSerializer):
    expenses = serializers.SerializerMethodField()

    class Meta:
        model = models.Cards
        fields = ['name', 'balance', 'card_brand', 'expenses']

    def get_expenses(self, obj):
        expenses = obj.expenses.all()
        return [
            {
                'name': expense.name,
                'amount': expense.amount,
                'currency': expense.currency,
                'payment_type': expense.payment_type,
                'purchase_date': expense.purchase_date,
                'status': expense.status,
            }
            for expense in expenses
        ]


class MonthlySummarySerializer(serializers.Serializer):
    month_date = serializers.DateField()
    total_in = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_out = serializers.DecimalField(max_digits=10, decimal_places=2)

