# Biblioteca Padrão
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


class CustomUser(AbstractUser, ModelBase, PermissionsMixin):
    username = models.CharField(
        db_column='username',
        max_length=50,
        unique=True,  # Necessário para evitar o erro
        validators=[MinLengthValidator(5)],
    )
    email = models.EmailField(
        db_column='email',
        max_length=255,
        unique=True,  # Opcional, caso o email seja usado como identificador
        validators=[EmailValidator()],
    )

    USERNAME_FIELD = 'username'  # Ou altere para 'email' se necessário
    REQUIRED_FIELDS = ['email']  # Caso altere o USERNAME_FIELD

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
