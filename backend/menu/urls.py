from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path('ingredient-list/', views.IngredientListView.as_view(), name='ingredient_list'),
    path('category-list/', views.CategoryListView.as_view(), name='category_list'),

    path('monthly-menu/', views.MonthlyMenuView.as_view(), name='monthly_menu'),

    # GENERIC LIST PATHS
    # URL pattern for editing a row
    path('edit/<int:pk>/<str:model_name>/', views.edit_row, name='edit_row'),
    # URL pattern for updating a row
    path('update/<int:pk>/<str:model_name>/', views.update_row, name='update_row'),
    # URL pattern for canceling an edit
    path('cancel/<int:pk>/<str:model_name>/', views.get_row, name='cancel_edit'),
    # URL pattern for deleting a row
    path('delete/<int:pk>/<str:model_name>/', views.delete_row, name='delete_row'),
]
