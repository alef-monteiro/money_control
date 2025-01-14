from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from finance import models


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializador para retornar informações do usuário.
    """

    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
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
        fields = ['username','first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Criação de usuário com senha criptografada
        user = models.CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)

        # Adicione os campos necessários ao payload
        token['id'] = user.id
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email

        return token

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categories
        fields = '__all__'

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model: models.Expenses
        fields = '__all__'

class CardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cards
        fields = '__all__'

