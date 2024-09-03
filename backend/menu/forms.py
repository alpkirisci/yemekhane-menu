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


    # Add bootstrap5 classes
    def __init__(self, *args, **kwargs):
        super(IngredientItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-dark text-light my-2'





IngredientItemFormSet = modelformset_factory(
    IngredientItem,
    form=IngredientItemForm,
    extra=10,
    can_delete=True,
    max_num=10,
)


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'calories', 'description', 'ingredients']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove 'ingredients' field from being rendered in the form
        # Will still be used in saving and validation
        self.fields.pop('ingredients')

        # Add bootstrap5 classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control bg-dark text-light my-2'

