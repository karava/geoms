"""gems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from knowledge_base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apis/', include("apis.urls")),
    # static pages
    path('', TemplateView.as_view(template_name='static_pages/index.html', extra_context=dict(page_title='Home')), name='home'),
    path('aboutus', TemplateView.as_view(template_name='static_pages/aboutus.html', extra_context=dict(page_title='About Us')), name='aboutus'),
    path('capabilities', TemplateView.as_view(template_name='static_pages/capabilities_statement.html', extra_context=dict(page_title='Capabilities Statement')), name='capabilities_statement'),
    path('products/', include('products.urls')),
    path('technical-guides/', views.technical_guide_list, name='technical_guide_list'),
    path('case-studies/', views.case_study_list, name='case_study_list'),
    path('case-studies/<slug:case_study_slug>/', views.case_study_detail, name='case_study_detail'),

]
