from django.urls import path
from . import views

app_name = 'catalog'  # добавляем app_name!

urlpatterns = [
    path('', views.home, name='home'),
    path('composition/<int:pk>/', views.composition_detail, name='composition_detail'),

    # Пока комментируем — чтобы не было ошибки
    # path('composition/add/', views.add_composition, name='add_composition'),
    # path('composition/<int:pk>/edit/', views.edit_composition, name='edit_composition'),
    # path('composition/<int:pk>/delete/', views.delete_composition, name='delete_composition'),
]
