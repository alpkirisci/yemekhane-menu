from django.db import models
from django.conf import settings

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# UnitType model
class UnitType(models.Model):
    name = models.CharField(max_length=50)  # e.g., grams, liters, pieces

    def __str__(self):
        return self.name

# IngredientName model
class IngredientName(models.Model):
    name = models.CharField(max_length=100)  # e.g., salt, carrot, tomato

    def __str__(self):
        return self.name

# Ingredient model
class Ingredient(models.Model):
    name = models.ForeignKey(IngredientName, on_delete=models.CASCADE)
    unit = models.IntegerField()  # Quantity of the ingredient
    unit_type = models.ForeignKey(UnitType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.unit} {self.unit_type.name} of {self.name.name}"

# MenuItem model
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    calories = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='menu_items_created')
    created_at = models.DateField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='menu_items_updated')
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

# DailyMenu model
class DailyMenu(models.Model):
    served_at = models.DateField()
    menu_items = models.ManyToManyField(MenuItem)
    servings = models.IntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='daily_menus_created')
    created_at = models.DateField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='daily_menus_updated')
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Menu for {self.served_at}"
