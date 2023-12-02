from django.urls import path
from .views import ProductDetailView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:category_slug>/', views.CategoryListView, name='product_category'),
    path('<str:category_slug>/<str:product_code>/', ProductDetailView.as_view(), name='product_detail'),
    path('contact/', views.product_enquiry, name='contact'),
]