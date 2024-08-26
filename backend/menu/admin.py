from django.contrib import admin
from .models import Category, IngredientItem, Ingredient, MenuItem, DailyMenu


class IngredientItemInline(admin.TabularInline):
    model = MenuItem.ingredients.through
    extra = 1


class MenuItemInline(admin.TabularInline):
    model = DailyMenu.menu_items.through
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(IngredientItem)
class IngredientItemAdmin(admin.ModelAdmin):
    list_display = ('ingredient',)
    search_fields = ('name__name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'calories', 'created_by', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at')

    inlines = [IngredientItemInline]
    exclude = ["ingredients"]


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    pass
    # list_display = ('served_at', 'created_by', 'servings', 'created_at')
    # search_fields = ('served_at',)
    # list_filter = ('served_at', 'created_at')
    #
    # inlines = [MenuItemInline]
    # exclude = ["menu_items"]