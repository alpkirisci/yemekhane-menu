from django import forms


def create_custom_model_form(model=None, fields=None, *args, **kwargs):
    pass_model = model
    pass_fields = fields
    class CustomModelForm(forms.ModelForm):
        class Meta:
            model = pass_model
            fields = '__all__'
    return CustomModelForm(*args, **kwargs)