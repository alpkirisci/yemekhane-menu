from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import CustomLoginForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def dashboard(request):
    return render(request, 'dashboard.html')


def login(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CustomLoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'dashboard.html')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomLoginForm()

    return render(request, "login.html", {"form": form})