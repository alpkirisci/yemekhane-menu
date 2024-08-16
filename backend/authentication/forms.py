from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    tshirt_color = forms.CharField(max_length=50, required=True)


    def clean(self):
        # Clean the form data without calling authenticate
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        tshirt_color = self.cleaned_data.get('tshirt_color')

        return self.cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tshirt_color'].widget.attrs.update({
            'placeholder': 'T-Shirt Color'
        })
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })

