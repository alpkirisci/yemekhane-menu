from datetime import datetime

from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("dashboard/ingredients", views.ingredients, name="ingredients"),

    # INGREDIENT PATHS
    path('dashboard/ingredients/list/', views.ingredient_list, name='ingredient-list'),
    path('dashboard/ingredients/list/<int:page>/', views.ingredient_table, name='ingredient-list'),
    path('dashboard/ingredients/list/<int:page>/<str:search_name>/', views.ingredient_table, name='ingredient-list'),


    path('dashboard/ingredients/list/get-row/<int:pk>/', views.ingredient_get_row, name='ingredient-get_row'),
    path('dashboard/ingredients/list/edit-row/', views.ingredient_edit_row, name='ingredient-edit_row'),
    path('dashboard/ingredients/list/edit-row/<int:pk>/', views.ingredient_edit_row, name='ingredient-edit_row'),
    path('dashboard/ingredients/list/update-row/<int:pk>/', views.ingredient_update_row, name='ingredient-update_row'),
    path('dashboard/ingredients/list/delete-row/<int:pk>/', views.ingredient_delete_row, name='ingredient-delete_row'),

    path("dashboard/ingredient-requirements/", views.ingredient_requirements, name="ingredient-requirements"),
    path("dashboard/ingredient-requirements/table/", views.ingredient_requirements_table, name="ingredient-requirements-table"),

    path("daily-menu/", views.daily_menu, name="daily_menu"),

    path("monthly-menu/", views.MenuMonthArchiveView.as_view(
        year=datetime.today().year, month=datetime.today().month
    ), name="monthly_menu", ),
    path("monthly-menu/<int:year>/<int:month>/", views.MenuMonthArchiveView.as_view(), name="monthly_menu",),


    # path('monthly-menu/', views.MonthlyMenuView.as_view(), name='monthly_menu'),

]
