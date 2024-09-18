from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    class UnitNames(models.TextChoices):
        GRAM = "g", _("Gram")
        MILLILITER = "ml", _("Milliliter")
        PIECES = "p", _("Piece(s)")

    name = models.CharField(max_length=50, unique=True, blank=False)
    unit = models.CharField(max_length=50, choices=UnitNames.choices, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class IngredientItem(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   limit_choices_to={'is_active': True},)

    quantity = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.1)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quantity} {self.ingredient} "


class MenuItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category,
                                   on_delete=models.CASCADE,
                                   limit_choices_to={'is_active': True},)

    calories = models.IntegerField()
    description = models.TextField(default="")
    ingredients = models.ManyToManyField(IngredientItem,
                                         limit_choices_to={'is_active': True},)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='created_menu_items')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='updated_menu_items')

    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class DailyMenu(models.Model):
    served_at = models.DateField(unique=True)
    menu_items = models.ManyToManyField(MenuItem,
                                   limit_choices_to={'is_active': True},)

    servings = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='created_daily_menus')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='updated_daily_menus')

    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Menu for {self.served_at}"
