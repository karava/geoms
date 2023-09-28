from django.urls import path
from .views import ProductDetailView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]