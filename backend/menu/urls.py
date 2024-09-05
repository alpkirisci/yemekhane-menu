from datetime import datetime

from django.urls import path, include
from . import views


ingredients_patterns = [
    path('', views.ingredients, name='ingredients_index'),
    path("container/", views.IngredientsListView.as_view(), name="ingredients_container"),
    path("list/", views.IngredientsListSearchView.as_view(), name="ingredients_list"),
    path("delete/<str:pk>/", views.IngredientsDeleteView.as_view(), name="ingredients_delete"),
    path("create/", views.IngredientsCreateView.as_view(), name="ingredients_create"),
    path("detail/<str:pk>/", views.IngredientsDetailView.as_view(), name="ingredients_detail"),
    path("update/<str:pk>/", views.IngredientsUpdateView.as_view(), name="ingredients_update"),
]

categories_patterns = [
    path('', views.categories, name='categories_index'),
    path("container/", views.CategoriesListView.as_view(), name="categories_container"),
    path("list/", views.CategoriesListSearchView.as_view(), name="categories_list"),
    path("delete/<str:pk>/", views.CategoriesDeleteView.as_view(), name="categories_delete"),
    path("create/", views.CategoriesCreateView.as_view(), name="categories_create"),
    path("detail/<str:pk>/", views.CategoriesDetailView.as_view(), name="categories_detail"),
    path("update/<str:pk>/", views.CategoriesUpdateView.as_view(), name="categories_update"),
]

menu_items_patterns = [
    path('', views.menu_items, name='menu_items_index'),
    path("container/", views.MenuItemsListView.as_view(), name="menu_items_container"),
    path("list/", views.MenuItemsListSearchView.as_view(), name="menu_items_list"),
    path("delete/<str:pk>/", views.MenuItemsDeleteView.as_view(), name="menu_items_delete"),
    path("detail/<str:pk>/", views.MenuItemsDetailView.as_view(), name="menu_items_detail"),
    path("create/", views.MenuItemsCreateView.as_view(), name="menu_items_create"),
    path("update/<str:pk>/", views.MenuItemsUpdateView.as_view(), name="menu_items_update"),
]

daily_menus_patterns = [

]

ingredient_requirements_patterns = [
    path("", views.ingredient_requirements,
         name="ingredient-requirements"),
    path("table/", views.ingredient_requirements_table,
         name="ingredient-requirements-table"),

]


dashboard_patterns = [
    path("", views.dashboard, name="dashboard"),
    path("ingredients/", include(ingredients_patterns)),
    path("categories/", include(categories_patterns)),
    path("menu_items/", include(menu_items_patterns)),
    path("daily_menus/", include(daily_menus_patterns)),
    path("ingredient_requirements/", include(ingredient_requirements_patterns)),

]

public_patterns = [
    path("daily-menu/", views.daily_menu, name="daily_menu"),
    path("monthly-menu/", views.MenuMonthArchiveView.as_view(
        year=datetime.today().year, month=datetime.today().month
    ), name="monthly_menu", ),

    path("monthly-menu/<int:year>/<int:month>/",
         views.MenuMonthArchiveView.as_view(),
         name="monthly_menu", ),
]


urlpatterns = [
    path("", views.dashboard, name="index"),
    path("dashboard/", include(dashboard_patterns)),
    path("public/", include(public_patterns)),
]
