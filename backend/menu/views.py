import calendar
from collections import defaultdict
from datetime import date

from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory, ModelForm, BaseForm
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, TemplateView, MonthArchiveView

from menu.models import Ingredient, Category, DailyMenu


from django.core.paginator import Paginator


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


@login_required
def ingredients(request):
    return render(request, 'dashboard/ingredients-list.html')


@login_required
def ingredient_requirements(request):
    return render(request, 'dashboard/ingredient-requirements/base.html')


class TableView:
    """
    To construct the model tables, views that depend on similar variables are used
    To DRY, TableView class will contain classes with similar dependencies and
    manage navigation for urls.py access
    """
    pass


def ingredient_list(request, *args, **kwargs):
    # ListView parameters
    model = Ingredient  # in-model: generic | inter-model: distinct
    template_name = 'generic/list.html' # in-model: generic | inter-model: generic
    paginate_by = 5 # in-model: generic | inter-model: generic

    # Parameters to pass to template
    # TODO: Need Translate
    list_title = 'Malzemeler' # in-model: generic | inter-model: distinct
    field_titles = ["İsim", "Birim"] # in-model: generic | inter-model: distinct
    # Make sure field_titles and fields match in order
    fields = ['name', 'unit'] # in-model: generic | inter-model: distinct

    # model_name will be used to not have duplicate row IDs when displaying multiple tables in a single page
    model_name = 'Ingredient' # in-model: generic | inter-model: distinct

    # rest:
    # in-model: generic | inter-model: generic
    items = model.objects.filter(is_active=True).order_by('-id') # in-model: generic | inter-model: generic

    paginator = Paginator(items, paginate_by)
    page_obj = paginator.get_page(1)

    context = {
        'page_obj': page_obj,
        'list_title': list_title,
        "field_titles": field_titles,
        'fields': fields,
        'model_name': model_name,
    }

    return TemplateResponse(request, template_name, context)


def ingredient_table(request, page = 1, *args, **kwargs):
    # ListView parameters
    model = Ingredient  # in-model: generic | inter-model: distinct
    template_name = 'generic/list-table.html' # in-model: generic | inter-model: generic
    paginate_by = 5 # in-model: generic | inter-model: generic

    # Parameters to pass to template
    # TODO: Need Translate
    list_title = 'Malzemeler' # in-model: generic | inter-model: distinct
    field_titles = ["İsim", "Birim"] # in-model: generic | inter-model: distinct
    # Make sure field_titles and fields match in order
    fields = ['name', 'unit'] # in-model: generic | inter-model: distinct

    # model_name will be used to not have duplicate row IDs when displaying multiple tables in a single page
    model_name = 'Ingredient' # in-model: generic | inter-model: distinct
    search_name = request.GET.get('search_name')
    # rest:
    # in-model: generic | inter-model: generic
    if search_name is not None and 3 <= len(search_name):
        items = model.objects.filter(name__icontains=search_name, is_active=True).order_by('-id') # in-model: generic | inter-model: generic
    else:
        items = model.objects.filter(is_active=True).order_by('-id') # in-model: generic | inter-model: generic

    paginator = Paginator(items, paginate_by)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'list_title': list_title,
        "field_titles": field_titles,
        'fields': fields,
        'model_name': model_name,
    }

    return TemplateResponse(request, template_name, context)


@login_required
def ingredient_get_row(request, pk):
    model = Ingredient  # generic in IngredientView
    fields = ['name', 'unit'] # generic in IngredientView
    model_name = 'Ingredient' # generic in IngredientView

    if request.method == 'GET':
        try:
            item = model.objects.get(pk=pk)
            return render(request, 'generic/get_row.html', {
                'item': item,
                'fields': fields,
                'model_name': model_name
            })
        except model.DoesNotExist:
            return HttpResponse('')


@login_required
def ingredient_edit_row(request, pk=None):
    model = Ingredient  # generic in IngredientView
    fields = ['name', 'unit'] # generic in IngredientView
    model_name = 'Ingredient' # generic in IngredientView

    if request.method == 'GET':
        if pk is not None:
            item = model.objects.get(pk=pk)
        else:
            pk = model.objects.latest('id').id + 1
            item = model(pk=pk)

        return render(request, 'generic/edit_row.html', {
            'item': item,
            'fields': fields,
            'model_name': model_name
        })


@login_required
def ingredient_delete_row(request, pk):
    model = Ingredient # generic in IngredientView
    item = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        item.is_active = False
        item.save()
        return HttpResponse('')

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def ingredient_update_row(request, pk):
    model = Ingredient  # generic in IngredientView
    fields = ['name', 'unit'] # generic in IngredientView
    model_name = 'Ingredient' # generic in IngredientView

    if request.method == 'PUT':
        CustomForm = modelform_factory(model=model, fields=fields)
        put_data = QueryDict(request.body.decode('utf-8'))

        try:
            item = model.objects.get(pk=pk)
        except model.DoesNotExist:
            item = model(pk=pk)

        form = CustomForm(put_data, instance=item)

        if form.is_valid():
            form.save()
            return render(request, 'generic/get_row.html', {
                'item': item,
                'fields': fields,
                'model_name': model_name,
            })
        else:
            return JsonResponse({'error': 'Invalid data submitted'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)






def ingredient_requirements_table(request):
    template_name = 'dashboard/ingredient-requirements/table.html'
    paginate_by = 1000000  # will handle pagination later

    # Parameters to pass to template
    field_titles = ["İsim", "Birim", "Gereken Miktar"]
    fields = ['name', 'unit', 'quantity_needed']

    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # get DailyMenu records with dates
        daily_menus = DailyMenu.objects.filter(served_at__range=[start_date, end_date])

        # defaultdict(int) rather than zeroing every key with this every accessed key that doesnt exist returns zero
        ingredient_quantities = defaultdict(int)

        for daily_menu in daily_menus:
            for menu_item in daily_menu.menu_items.all():
                for ingredient_item in menu_item.ingredients.all():
                    # defaultdict is used here in case it wasn't clear
                    ingredient_quantities[ingredient_item.ingredient] += ingredient_item.quantity

        # done to not change the template too much in case of other report needs prone to change
        # instead of this we can just add ingredient_quantities to the template context
        ingredients = Ingredient.objects.filter(id__in=[ingredient.id for ingredient in ingredient_quantities.keys()])
        for ingredient in ingredients:
            ingredient.quantity_needed = ingredient_quantities[ingredient]

        # pagination will be done later after getting the OK
        paginator = Paginator(ingredients, paginate_by)
        page_obj = paginator.get_page(1)

        context = {
            'page_obj': page_obj,
            "field_titles": field_titles,
            'fields': fields,
        }

        return TemplateResponse(request, template_name, context)












class CategoryListView(ListView):
    # ListView parameters
    model = Category    # distinct
    template_name = 'generic/list.html' #generic
    paginate_by = 5     #generic

    # Parameters to pass to template
    # TODO: Need Translate
    list_title = 'Yemek Kategorileri'   # distinct
    field_titles = ["İsim"]     # distinct
    # Make sure field_titles and fields match in order
    fields = ['name']       # distinct

    # model_name will be used to not have duplicate row IDs when displaying multiple tables in a single page
    model_name = 'Category'   # distinct

    # generic method
    def get_context_data(self, **kwargs):
        # load the Ingredient records and pagination
        context = super().get_context_data(**kwargs)

        context['list_title'] = self.list_title
        context["field_titles"] = self.field_titles
        context['fields'] = self.fields
        context['model_name'] = self.model_name
        return context


@login_required
def category_get_row(request, pk):
    model = Category  # generic in CategoryView
    item = get_object_or_404(model, pk=pk)
    fields = ['name',] # generic in CategoryView
    model_name = 'Category' # generic in CategoryView
    return render(request, 'generic/get_row.html', {
        'item': item,
        'fields': fields,
        'model_name': model_name
    })














class MenuMonthArchiveView(MonthArchiveView):
    queryset = DailyMenu.objects.all()
    date_field = "served_at"
    allow_future = True
    allow_empty = True
    context_object_name = 'daily_menus'
    template_name = "public/monthly_menu.html"
    month_format = "%m"

    categories = Category.objects.all().order_by('-order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.get_year()
        month = self.get_month()
        cal = calendar.Calendar()
        month_calendar = [
            [datetime(year, month, day) if day != 0 else None for day in week]
            for week in cal.monthdayscalendar(year, month)
        ]
        context['calendar'] = month_calendar
        context['categories'] = self.categories
        return context


def daily_menu(request):
    today = date.today()
    template_name = 'public/daily_menu.html'
    categories = Category.objects.all().order_by('-order')

    try:
        menu = DailyMenu.objects.get(served_at=today)
    except DailyMenu.DoesNotExist:
        menu = None

    return render(request, template_name, {
        'today': today,
        'menu': menu,
        'categories': categories,
    })