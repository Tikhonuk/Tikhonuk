from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('composition/<int:pk>/', views.composition_detail, name='composition_detail'),
]
