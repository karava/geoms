from django.urls import path
from .views import ProductDetailView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category, name='product_category'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contact/', views.product_enquiry, name='contact'),
]