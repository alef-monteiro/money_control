# Biblioteca Padrão
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Biblioteca Terceiros
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinValueValidator, MinLengthValidator, EmailValidator


class ModelBase(models.Model):
    id = models.BigAutoField(
        db_column='id',
        primary_key=True,
    )
    created_at = models.DateTimeField(
        db_column='dt_created_at',
        auto_now_add=True,
        verbose_name="Data de Criação",
    )
    modified_at = models.DateTimeField(
        db_column='dt_modified_at',
        auto_now=True,
        verbose_name="Última Modificação",
    )
    active = models.BooleanField(
        db_column='cs_active',
        default=True,
    )

    class Meta:
        abstract = True
        managed = True


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Garantir que o superusuário tenha as permissões de staff e superusuário
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Não precisa mais de username, então passamos só o email
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin, ModelBase):
    # Usando email como identificador
    username = models.CharField(
        max_length=50,
        unique=True,
        blank=True,  # Permite o campo username em branco
    )
    email = models.EmailField(
        max_length=255,
        unique=True,  # O email será o identificador único
    )

    # Mudando o campo principal para 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Não incluir 'username'

    # Define o UserManager para o modelo
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Cards(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cards',
    )
    name = models.CharField(max_length=100)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],  # Validação para evitar valores negativos
    )
    card_brand = models.CharField(max_length=100)

    def __str__(self):
        return self.card_brand


class Categories(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Expenses(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='expenses',
    )
    card = models.ForeignKey(
        Cards,
        on_delete=models.CASCADE,
        related_name='expenses',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.DO_NOTHING,
        related_name='expenses',
    )
    name = models.CharField(max_length=20)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    currency = models.CharField(max_length=10)
    payment_type = models.CharField(max_length=20)
    purchase_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20)

    def clean(self):
        if self.due_date < self.purchase_date:
            raise ValueError("A data de vencimento não pode ser anterior à data de compra.")

    def __str__(self):
        return f"{self.name} - {self.amount} {self.currency}"
