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
from django.views.static import serve
from django.conf import settings

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apis/', include("apis.urls")),
    # static pages
    path('', views.index, name='home'),
    path('aboutus', TemplateView.as_view(template_name='static_pages/aboutus.html', extra_context=dict(page_title='About Us')), name='aboutus'),
    path('capabilities', TemplateView.as_view(template_name='static_pages/capabilities_statement.html', extra_context=dict(page_title='Capabilities Statement')), name='capabilities_statement'),
    path('contact', views.product_enquiry, name='contact'),
    path('applications', views.render_applications, name='applications'),
    path('applications/<slug:slug>/', views.render_application_detail, name='application_detail'),
    path('products/', include('products.urls')),
    path('knowledgebase/', include('knowledge_base.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('sitemap.xml', serve, {'path': 'assets/sitemap.xml', 'document_root': settings.STATIC_ROOT}),
]
