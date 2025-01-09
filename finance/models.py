# Biblioteca Padrão
from django.db import models

# Biblioteca Terceiros
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import  MinValueValidator, MaxValueValidator


class ModelBase(models.Model):
    id = models.BigAutoField(
        db_column='id',
        null=False,
        primary_key=True,
    )
    created_at = models.DateTimeField(
        db_column='dt_created_at',
        auto_now_add=True,
        verbose_name="Data de Criação",
        null=False,
    )
    modified_at = models.DateTimeField(
        db_column='dt_modified_at',
        auto_now=True,
        verbose_name="Última modificação",
        null=False,
    )
    active = models.BooleanField(
        db_column='cs_active',
        default=True,
        null=False,
    )

    class Meta:
        abstract = True
        managed = True


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, ModelBase, PermissionsMixin):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Cards(models.Model):
    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    balance = models.DecimalField(
        max_digits=10,  # Total de dígitos (incluindo casas decimais)
        decimal_places=2,  # Quantidade de casas decimais
        blank=False,
        null=False,
    )
    card_brand = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    def __str__(self):
        return f"{self.card_brand} {self.balance}"


class Categories(models.Model):
    name = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )


class Expenses(models.Model):
    user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    card_id = models.ForeignKey(
        Cards,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    category_id = models.ForeignKey(
        Categories,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
    )
    name = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        null=False,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    currency = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    payment_type = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )
    purchase_date = models.DateField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    due_date = models.DateField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    status = models.CharField(
        max_length=20,
        blank=False,
        null=False,
    )
