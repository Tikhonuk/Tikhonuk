from django.urls import path
from . import views

app_name = 'catalog'  # важная строка!

urlpatterns = [
    path('', views.home, name='home'),
    path('composition/<int:pk>/', views.composition_detail, name='composition_detail'),
    path('composition/add/', views.composition_add, name='composition_add'),
    path('composition/<int:pk>/edit/', views.composition_edit, name='composition_edit'),
    path('composition/<int:pk>/delete/', views.composition_delete, name='composition_delete'),
]