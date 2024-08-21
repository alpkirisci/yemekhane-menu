from django import forms


def create_custom_model(model, *args, **kwargs):
    model_transit = model
    class CustomModelForm(forms.ModelForm):
        class Meta:
            model = model_transit
            fields = '__all__'
    return CustomModelForm(*args, **kwargs)