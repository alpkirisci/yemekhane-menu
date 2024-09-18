from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ingredient, IngredientItem, MenuItem, DailyMenu


# Soft-delete cascades
@receiver(post_save, sender=Ingredient)
def deactivate_ingredient_items(sender, instance, **kwargs):
    if not instance.is_active:
        # Set related IngredientItem instances to inactive
        IngredientItem.objects.filter(ingredient=instance).update(is_active=False)

@receiver(post_save, sender=IngredientItem)
def remove_inactive_ingredient_item(sender, instance, **kwargs):
    if not instance.is_active:
        # Remove inactive IngredientItem from all MenuItem objects
        MenuItem.objects.filter(ingredients=instance).update(ingredients=None)

@receiver(post_save, sender=MenuItem)
def remove_inactive_menu_item(sender, instance, **kwargs):
    if not instance.is_active:
        # Remove inactive MenuItem from all DailyMenu objects
        DailyMenu.objects.filter(menu_items=instance).update(menu_items=None)