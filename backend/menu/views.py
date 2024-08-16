from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')



