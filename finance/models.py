# Biblioteca Padrão
from django.db import models

# Biblioteca Terceiros
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


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


class CustomUser(AbstractUser, ModelBase, PermissionsMixin):
    password = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(6)
        ],
        blank=False,
    )

    # Estes dois atributos são para evitar conflitos de nomenclatura entre AbstractUser e auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Nome diferente
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Nome diferente
        blank=True,
    )

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
        return f"{self.card_brand}"


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
