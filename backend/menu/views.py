import calendar
from collections import defaultdict
from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, MonthArchiveView, CreateView, DeleteView, \
    DetailView, UpdateView

from menu.forms import IngredientForm, CategoryForm, MenuItemForm, IngredientItemForm
from menu.models import Ingredient, Category, DailyMenu, MenuItem, IngredientItem


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def categories(request):
    return render(request, 'dashboard/categories/index.html')

@login_required
def ingredients(request):
    return render(request, 'dashboard/ingredients/index.html')

@login_required
def menu_items(request):
    return render(request, 'dashboard/menu_items/index.html')

@login_required
def ingredient_requirements(request):
    return render(request, 'dashboard/ingredient-requirements/base.html')


def ingredient_requirements_table(request):
    """ Calculate needed ingredients within given date range and display. """
    template_name = 'dashboard/ingredient-requirements/table.html'
    paginate_by = 1000000  # Pagination currently on client-side.

    # Parameters to pass to template.
    field_titles = ["İsim", "Birim", "Gereken Miktar"]
    fields = ['name', 'unit', 'quantity_needed']

    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Get DailyMenu records with dates.
        daily_menus = DailyMenu.objects.filter(served_at__range=[start_date, end_date])

        # defaultdict(int) better than zeroing every value.
        # Every accessed key that does not exist returns zero.
        ingredient_quantities = defaultdict(int)

        for daily_menu in daily_menus:
            for menu_item in daily_menu.menu_items.all():
                for ingredient_item in menu_item.ingredients.all():
                    # defaultdict is used here in case it wasn't clear.
                    ingredient_quantities[ingredient_item.ingredient] += ingredient_item.quantity * daily_menu.servings

        # OR instead, just add ingredient_quantities to paginator.
        ingredients = Ingredient.objects.filter(id__in=[ingredient.id for ingredient in ingredient_quantities.keys()])
        for ingredient in ingredients:
            ingredient.quantity_needed = ingredient_quantities[ingredient]

        # Pagination currently done on the client-side.
        paginator = Paginator(ingredients, paginate_by)
        page_obj = paginator.get_page(1)

        context = {
            'page_obj': page_obj,
            "field_titles": field_titles,
            'fields': fields,
        }

        return TemplateResponse(request, template_name, context)


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


class IngredientsListView(ListView):
    model = Ingredient
    template_name = 'dashboard/ingredients/container.html'
    paginate_by = 5
    ordering = '-id'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class IngredientsListSearchView(IngredientsListView):
    template_name = 'dashboard/ingredients/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name = self.request.GET.get('search_name')
        if search_name is not None:
            return queryset.filter(name__icontains=search_name)
        return queryset


class IngredientsDeleteView(DeleteView):
    model = Ingredient
    template_name = 'dashboard/ingredients/confirm_delete.html'

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect('menu:ingredients_list')


class IngredientsDetailView(DetailView):
    model = Ingredient
    template_name = 'dashboard/ingredients/detail.html'


class IngredientsCreateView(CreateView):
    model = Ingredient
    template_name = 'dashboard/ingredients/create.html'
    form_class = IngredientForm

    def get_success_url(self):
        pk = self.object.id
        return reverse("menu:ingredients_detail", kwargs={"pk": pk})


class IngredientsUpdateView(UpdateView):
    model = Ingredient
    template_name = 'dashboard/ingredients/update.html'
    form_class = IngredientForm

    def get_success_url(self):
        pk = self.object.id
        return reverse("menu:ingredients_detail", kwargs={"pk": pk})


class CategoriesListView(ListView):
    model = Category
    template_name = 'dashboard/categories/container.html'
    paginate_by = 5
    ordering = 'order'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class CategoriesListSearchView(CategoriesListView):
    template_name = 'dashboard/categories/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name = self.request.GET.get('search_name')
        if search_name is not None:
            return queryset.filter(name__icontains=search_name)
        return queryset


class CategoriesDeleteView(DeleteView):
    model = Category
    template_name = 'dashboard/categories/confirm_delete.html'

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect('menu:ingredients_list')


class CategoriesDetailView(DetailView):
    model = Category
    template_name = 'dashboard/categories/detail.html'


class CategoriesCreateView(CreateView):
    model = Category
    template_name = 'dashboard/categories/create.html'
    form_class = CategoryForm

    def get_success_url(self):
        pk = self.object.id
        return reverse("menu:categories_detail", kwargs={"pk": pk})


class CategoriesUpdateView(UpdateView):
    model = Category
    template_name = 'dashboard/categories/update.html'
    form_class = CategoryForm

    def get_success_url(self):
        pk = self.object.id
        return reverse("menu:categories_detail", kwargs={"pk": pk})


class MenuItemsListView(ListView):
    model = MenuItem
    template_name = 'dashboard/menu_items/container.html'
    paginate_by = 5
    ordering = '-id'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class MenuItemsListSearchView(MenuItemsListView):
    template_name = 'dashboard/menu_items/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name = self.request.GET.get('search_name')
        if search_name is not None:
            return queryset.filter(name__icontains=search_name)
        return queryset


class MenuItemsDeleteView(DeleteView):
    model = MenuItem
    template_name = 'dashboard/menu_items/confirm_delete.html'

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect('menu:menu_items_list')


class MenuItemsDetailView(DetailView):
    model = MenuItem
    template_name = 'dashboard/menu_items/detail.html'


def get_ingredient_items_formset(request):
    """ To manage GET for ingredient items in MenuItemsCreate/Update """
    IngredientItemFormSet = modelformset_factory(
        IngredientItem,
        form=IngredientItemForm,
        extra=1,
        can_delete=True,
    )
    if request.method == "GET":
        pk = request.GET.get('pk')
        if pk is not None:
        # Then this is an update view GET
            formset = IngredientItemFormSet(queryset=MenuItem.objects.get(pk=pk).ingredients.all())
        else:
        # Then this is a create view GET
            formset = IngredientItemFormSet(queryset=IngredientItem.objects.none())
        return formset
    raise Http404('Method not allowed')


# def post_ingredient_items_formset(request, kwargs):
#     """ To manage POST for ingredient items in MenuItemsCreate/Update """
#     IngredientItemFormSet = modelformset_factory(
#         IngredientItem,
#         form=IngredientItemForm,
#         extra=1,
#         can_delete=True,
#     )
#     # Save IngredientItem
#     # TODO: Save IngredientItem to MenuItem
#     if request.method == "POST":
#         formset = IngredientItemFormSet(request.POST)
#         if formset.is_valid():
#             formset.save()
#             main_form = kwargs.get('form')
#         return formset
#     raise Http404('Method not allowed')


class MenuItemsCreateView(CreateView):
    model = MenuItem
    template_name = 'dashboard/menu_items/create.html'
    form_class = MenuItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = get_ingredient_items_formset(self.request)
        return context


class MenuItemsUpdateView(UpdateView):
    model = MenuItem
    template_name = 'dashboard/menu_items/update.html'
    form_class = MenuItemForm