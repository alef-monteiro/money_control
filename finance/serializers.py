from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from finance import models


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializador para retornar informações do usuário.
    """

    class Meta:
        model = models.CustomUser
        fields = [ 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def create(self, validated_data):
            # Criação de usuário com senha criptografada
            user = models.CustomUser.objects.create_user(validated_data)
            return user

    # # Teste
    # def __init__(self, instance=None, data=empty, **kwargs):
    #     super().__init__(instance, data, kwargs)
    #     self.last_name = None
    #     self.first_name = None

    # def create(self, validated_data):
    #     # Criação de usuário com senha criptografada
    #     user = models.CustomUser(
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #         email=validated_data['email'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    # # Teste
    # def get_full_name(self):
    #     return self.first_name + ' ' + self.last_name


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Criação de usuário com senha criptografada
        user = models.CustomUser(
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
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cards
        fields = '__all__'

