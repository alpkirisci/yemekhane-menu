from decimal import Decimal

from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from menu.models import Ingredient, Category, MenuItem, IngredientItem, DailyMenu


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'order']


class IngredientSelect(forms.Select):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value:
            option["attrs"]["data-unit"] = value.instance.get_unit_display()
        return option


class IngredientItemForm(forms.ModelForm):
    class Meta:
        model = IngredientItem
        fields = ['ingredient', 'quantity']
        widgets = {"ingredient": IngredientSelect}

    def __init__(self, *args, **kwargs):
        super(IngredientItemForm, self).__init__(*args, **kwargs)

        # Add bootstrap5 classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-dark text-light my-2'

    def clean_quantity(self):
        """Check if the quantity is in valid quarters"""
        quantity = self.cleaned_data['quantity']
        if quantity % Decimal('0.25') != 0:
            raise forms.ValidationError('The quantity must be in quarters (e.g., .00, .25, .50, .75).')
        return quantity


IngredientItemFormSet = modelformset_factory(
    IngredientItem,
    form=IngredientItemForm,
    extra=1,
    can_delete=True,
)


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'calories', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add bootstrap5 classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-dark text-light my-2'


class MenuItemSelectForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ('name',)
        widgets = {
        }

MenuItemFormSet = modelformset_factory(
    MenuItem,
    form=MenuItemSelectForm,
    extra=1,
    can_delete=True,
)

class DailyMenuForm(forms.ModelForm):
    class Meta:
        model = DailyMenu
        fields = ['served_at', 'servings',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add bootstrap5 classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-dark text-light my-2'

