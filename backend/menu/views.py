from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, TemplateView

from menu.forms import create_custom_model
from menu.models import Ingredient, Category, DailyMenu

from django.apps import apps
from django.http import Http404


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


class CustomListView(ListView):
    model = None
    list_title = None
    attr_titles = None

    def get(self, request, *args, **kwargs):
        # Get the model's fields and verbose names
        fields = [field.name for field in self.model._meta.fields if field.name != 'id']

        # Fetch all ingredients
        items = self.model.objects.all().order_by('id')

        # Pass the fields and headers to the template
        return render(request, self.template_name, {
            'model_name': self.model.__name__,
            'items': items,
            'fields': fields,
            'list_title': self.list_title,
            'attr_titles': self.attr_titles,
        })

class IngredientListView(CustomListView):
    model = Ingredient
    template_name = 'generic/list.html'  # Your template
    # TODO: Need Translate
    list_title = 'Malzemeler'
    attr_titles = ["İsim", "Birim"]

class CategoryListView(CustomListView):
    model = Category
    template_name = 'generic/list.html'  # Your template
    list_title = 'Yemek Kategorileri'
    attr_titles = ["İsim"]


def edit_row(request, pk, model_name):
    model = get_model_by_name(model_name)
    item = get_object_or_404(model, pk=pk)
    fields = [field.name for field in model._meta.fields if field.name != 'id']
    return render(request, 'generic/edit_row.html', {
        'item': item,
        'fields': fields,
        'model_name': model_name
    })


def get_row(request, pk, model_name):
    model = get_model_by_name(model_name)
    item = get_object_or_404(model, pk=pk)
    fields = [field.name for field in model._meta.fields if field.name != 'id']
    return render(request, 'generic/get_row.html', {
        'item': item,
        'fields': fields,
        'model_name': model_name
    })


@login_required
def update_row(request, pk, model_name):
    model = get_model_by_name(model_name)  # Custom function to get the model class by name
    item = get_object_or_404(model, pk=pk)
    fields = [field.name for field in model._meta.fields if field.name != 'id']

    if request.method == 'PUT':
        # Manually parse the form-encoded data from request.body
        put_data = QueryDict(request.body.decode('utf-8'))

        # Create a form instance with the parsed data and the existing item instance
        form = create_custom_model(model, put_data, instance=item)

        if form.is_valid():
            form.save()
            return render(request, 'generic/get_row.html', {'item': item, 'model_name': model_name, 'fields': fields})
        else:
            # If the form is not valid, return an error response
            return JsonResponse({'error': 'Invalid data submitted'}, status=400)

    # Handle other methods or return an error if method is not allowed
    return JsonResponse({'error': 'Method not allowed'}, status=405)



@login_required
def delete_row(request, pk, model_name):
    model = get_model_by_name(model_name)  # Custom function to get the model class by name
    item = get_object_or_404(model, pk=pk)

    if request.method == 'DELETE':
        item.delete()
        return HttpResponse('')

    # Handle other methods or return an error if method is not allowed
    return JsonResponse({'error': 'Method not allowed'}, status=405)



# ONLY WORKS WITH THE MENU APP
# only use with generic methods or views
def get_model_by_name(model_name):
    try:
        return apps.get_model(app_label="menu", model_name=model_name)
    except LookupError:
        raise Http404(f"Model '{model_name}' does not exist.")


class MonthlyMenuView(TemplateView):
    template_name = 'public/monthly_menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.today()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        month_objects = DailyMenu.objects.filter(served_at__month=today.month, served_at__year=today.year)

        current_month_days = []
        for day in range(first_day_of_month.day, last_day_of_month.day + 1):
            current_day = first_day_of_month.replace(day=day)

            try:
                daily_menu = month_objects.get(served_at=current_day)

            except DailyMenu.DoesNotExist:
                daily_menu = None

            current_month_days.append({'date': current_day, 'menu': daily_menu})

        context['current_month_days'] = current_month_days
        return context
