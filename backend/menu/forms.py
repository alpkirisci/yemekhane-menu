from django import forms


def CustomModelFormFactory(model, *args, **kwargs):
    Model = model
    class CustomModelForm(forms.ModelForm):
        class Meta:
            model = Model
            fields = '__all__'
    return CustomModelForm(*args, **kwargs)