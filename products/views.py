import os, json
from django.conf import settings
from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import BaseProduct

# Create your views here.

def index(request):
    path = os.path.join(settings.BASE_DIR, 'data')

    file_name = "products.json"
    json_url = "%s/%s" % (path, file_name)
    items = json.load(open(json_url))

    context = {'categories': items, 'page_title': 'Product Categories'}
    return render(request, 'index.html', context)

def category(request, slug):
    context = {}
    return render(request, 'category.html', context)

class ProductDetailView(DetailView):
    model = BaseProduct
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['default_image'] = self.object.images.filter(is_default=True).first()
        context['website_images'] = self.object.images.filter(is_for_website=True)
        context['model_name'] = self.object.get_product_detail_name()
        context['resources'] = self.object.resources.all()
        return context

