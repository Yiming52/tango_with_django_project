from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # About page
    path('about/', views.about, name='about'),
    # Add a new category
    path('add_category/', views.add_category, name='add_category'),
    # Show a specific category by its slug
    path('category/<str:category_name_slug>/', views.show_category, name='show_category'),
]
