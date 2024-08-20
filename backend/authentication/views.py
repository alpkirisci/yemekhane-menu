from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from .forms import CustomAuthenticationForm
from django.urls import reverse


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'

# if the user is logged in redirect to dashboard
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('menu:dashboard'))
        return super().dispatch(request, *args, **kwargs)



    def form_valid(self, form):

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


# Redirect to the login page after logout
def custom_logout(request):
    logout(request)

