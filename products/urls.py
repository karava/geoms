from django.urls import path
from .views import ProductDetailView

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:category_slug>/', views.CategoryListView, name='product_category'),
    path('<str:category_slug>/<str:product_code>/', ProductDetailView.as_view(), name='product_detail'),
]