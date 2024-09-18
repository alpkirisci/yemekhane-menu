import calendar
from collections import defaultdict
from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, MonthArchiveView, CreateView, DeleteView, \
    DetailView, UpdateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ProcessFormView, ModelFormMixin

from menu.forms import IngredientForm, CategoryForm, MenuItemForm, IngredientItemFormSet, DailyMenuForm, MenuItemFormSet
from menu.formset_views import FormSetUpdateView, FormSetCreateView
from menu.models import Ingredient, Category, DailyMenu, MenuItem, IngredientItem


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


@login_required
def ingredient_requirements(request):
    return render(request, 'dashboard/ingredient_requirements/base.html')

def ingredient_requirements_table(request):
    """Calculate needed ingredients within given date range and display."""
    # TODO: Review ingredient_requirements_table
    template_name = 'dashboard/ingredient_requirements/table.html'
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
    """"""
    # TODO: Review MonthArchiveView
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


def public_daily_menu(request):
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

@login_required
def ingredients(request):
    return render(request, 'dashboard/ingredients/index.html')


class IngredientsListView(ListView):
    """Construct ingredients list."""
    model = Ingredient
    template_name = 'dashboard/ingredients/container.html'
    paginate_by = 5
    ordering = '-id'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class IngredientsListSearchView(IngredientsListView):
    """Construct ingredients list with search."""
    template_name = 'dashboard/ingredients/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name = self.request.GET.get('search_name')
        if search_name is not None:
            return queryset.filter(name__icontains=search_name)
        return queryset


class IngredientsDeleteView(DeleteView):
    """Confirmation form and delete logic for ingredients record."""
    model = Ingredient
    template_name = 'dashboard/ingredients/confirm_delete.html'

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect('menu:ingredients_list')


class IngredientsDetailView(DetailView):
    """Construct ingredients record for display."""
    model = Ingredient
    template_name = 'dashboard/ingredients/detail.html'


class IngredientsCreateView(CreateView):
    """Construct ingredients form for creation."""
    model = Ingredient
    template_name = 'dashboard/ingredients/create.html'
    form_class = IngredientForm

    def get_success_url(self):
        pk = self.object.id
        return reverse("menu:ingredients_detail", kwargs={"pk": pk})


class IngredientsUpdateView(UpdateView):
    """Construct ingredients form for updates."""
    model = Ingredient
    template_name = 'dashboard/ingredients/update.html'
    form_class = IngredientForm

    def get_success_url(self):
        pk = self.object.id
        return reverse("menu:ingredients_detail", kwargs={"pk": pk})


@login_required
def categories(request):
    return render(request, 'dashboard/categories/index.html')


class CategoriesListView(ListView):
    """Construct categories list."""
    model = Category
    template_name = 'dashboard/categories/container.html'
    paginate_by = 5
    ordering = 'order'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class CategoriesListSearchView(CategoriesListView):
    """Construct categories list with search."""
    template_name = 'dashboard/categories/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name = self.request.GET.get('search_name')
        if search_name is not None:
            return queryset.filter(name__icontains=search_name)
        return queryset


class CategoriesDeleteView(DeleteView):
    """Confirmation form and delete logic for ingredients record."""
    model = Category
    template_name = 'dashboard/categories/confirm_delete.html'

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect('menu:ingredients_list')


class CategoriesDetailView(DetailView):
    """Construct categories record for display."""
    model = Category
    template_name = 'dashboard/categories/detail.html'


class CategoriesCreateView(CreateView):
    """Construct ingredients form for creation."""
    model = Category
    template_name = 'dashboard/categories/create.html'
    form_class = CategoryForm

    def get_success_url(self):
        pk = self.object.id
        return reverse("menu:categories_detail", kwargs={"pk": pk})


class CategoriesUpdateView(UpdateView):
    """Construct ingredients form for updates."""
    model = Category
    template_name = 'dashboard/categories/update.html'
    form_class = CategoryForm

    def get_success_url(self):
        pk = self.object.id
        return reverse("menu:categories_detail", kwargs={"pk": pk})


@login_required
def menu_items(request):
    return render(request, 'dashboard/menu_items/index.html')


class MenuItemsListView(ListView):
    """Construct menu_items list."""
    model = MenuItem
    template_name = 'dashboard/menu_items/container.html'
    paginate_by = 5
    ordering = '-id'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class MenuItemsListSearchView(MenuItemsListView):
    """Construct menu_items list with search."""
    template_name = 'dashboard/menu_items/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name = self.request.GET.get('search_name')
        if search_name is not None:
            return queryset.filter(name__icontains=search_name)
        return queryset


class MenuItemsDeleteView(DeleteView):
    """Confirmation form and delete logic for menu_items record."""
    model = MenuItem
    template_name = 'dashboard/menu_items/confirm_delete.html'

    def form_valid(self, form):
        self.object.is_active = False
        self.object.save()
        return redirect('menu:menu_items_list')


class MenuItemsDetailView(DetailView):
    """Construct menu_items record for display."""
    model = MenuItem
    template_name = 'dashboard/menu_items/detail.html'


class MenuItemsUpdateView(FormSetUpdateView):
    model = MenuItem
    template_name = 'dashboard/menu_items/update.html'
    form_class = MenuItemForm
    success_url = reverse_lazy('menu:menu_items_index')
    formset_class = IngredientItemFormSet
    formset_related_field = 'ingredients'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class MenuItemsCreateView(FormSetCreateView):
    model = MenuItem
    template_name = 'dashboard/menu_items/create.html'
    form_class = MenuItemForm
    success_url = reverse_lazy('menu:menu_items_index')
    formset_class = IngredientItemFormSet
    formset_related_field = 'ingredients'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@login_required
def daily_menus(request):
    return render(request, 'dashboard/daily_menus/index.html')


class DailyMenusListView(ListView):
    """Construct menu_items list."""
    model = DailyMenu
    template_name = 'dashboard/daily_menus/container.html'
    paginate_by = 5
    ordering = '-id'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class DailyMenusListSearchView(DailyMenusListView):
    """Construct menu_items list with search."""
    template_name = 'dashboard/daily_menus/list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            queryset = queryset.filter(served_at__range=[start_date, end_date])
        return queryset


# class MenuItemsDeleteView(DeleteView):
#     """Confirmation form and delete logic for menu_items record."""
#     model = MenuItem
#     template_name = 'dashboard/menu_items/confirm_delete.html'
#
#     def form_valid(self, form):
#         self.object.is_active = False
#         self.object.save()
#         return redirect('menu:menu_items_list')
#
#
class DailyMenusDetailView(DetailView):
    """Construct menu_items record for display."""
    model = DailyMenu
    template_name = 'dashboard/daily_menus/detail.html'

#
# class MenuItemsUpdateView(FormSetUpdateView):
#     model = MenuItem
#     template_name = 'dashboard/menu_items/update.html'
#     form_class = MenuItemForm
#     success_url = reverse_lazy('menu:menu_items_index')
#     formset_class = IngredientItemFormSet
#     formset_related_field = 'ingredients'
#
#     def form_valid(self, form):
#         """Assign the current user to the updated_by field."""
#         form.instance.updated_by = self.request.user
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)
#
#
class DailyMenusCreateView(FormSetCreateView):
    # TODO
    model = DailyMenu
    template_name = 'dashboard/daily_menus/create.html'
    form_class = DailyMenuForm
    success_url = reverse_lazy('menu:daily_menus_index')
    formset_class = MenuItemFormSet
    formset_related_field = 'menu_items'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)


