from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse

from .forms import CustomAuthenticationForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'


    def post(self, request, *args, **kwargs):
        # Print out the POST data for debugging
        print("POST data:", request.POST)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # Ensure that all form data is being processed correctly
        print(50 * "*")
        print("Form is valid. Cleaned data:", form.cleaned_data)
        print(50 * "*")

        user = authenticate(
            request=self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            tshirt_color=form.cleaned_data['tshirt_color']
        )
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid password. Please try again.")
            return self.form_invalid(form)


def custom_logout(request):
    # Redirect to the login page after logout
    logout(request)
