from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from menu.models import Ingredient, Category, MenuItem, IngredientItem


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'order']


class IngredientItemForm(forms.ModelForm):
    class Meta:
        model = IngredientItem
        fields = ['ingredient', 'quantity']

    # Add bootstrap5 classes
    def __init__(self, *args, **kwargs):
        super(IngredientItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-dark text-light mb-2'


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'calories', 'description']

    # Add bootstrap5 classes
    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-dark text-light mb-2'