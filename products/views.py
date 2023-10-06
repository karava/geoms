import os, json
from django.conf import settings
from django.shortcuts import render
from django.views.generic import DetailView
from .models import BaseProduct, Geocell, Geogrid, Geotextile, GCL, DrainageProduct, ImageFile
from django.db.models import Prefetch

# Create your views here.

def index(request):
    path = os.path.join(settings.BASE_DIR, 'data')

    file_name = "products.json"
    json_url = "%s/%s" % (path, file_name)
    items = json.load(open(json_url))

    context = {'categories': items, 'page_title': 'Product Categories'}
    return render(request, 'index.html', context)

# def category(request, slug):
#     context = {}
#     return render(request, 'category.html', context)

def category(request, slug):
    # Map slugs to their respective models and OneToOneField names in BaseProduct
    slug_to_model = {
        'geocells': (Geocell, 'product_detail_geocell'),
        'gcls': (GCL, 'product_detail_gcl'),
        'geotextiles': (Geotextile, 'product_detail_geotextile'),
        'geogrids': (Geogrid, 'product_detail_geogrid'),
        'drainage_systems': (DrainageProduct, 'product_detail_drainage'),
    }

    # Check if the provided slug is valid
    if slug not in slug_to_model:
        # Handle invalid slugs (you can render an error page or raise a 404)
        return render(request, 'error_page.html', {'message': 'Invalid category.'})

    # Fetch the related model and its field name in BaseProduct
    related_model, related_field_name = slug_to_model[slug]

    # Get all base products that have the related model set
    products = BaseProduct.objects.filter(**{f"{related_field_name}__isnull": False})

    # Prefetch related default images
    default_images = ImageFile.objects.filter(is_default=True)
    products = products.prefetch_related(Prefetch('images', queryset=default_images, to_attr='default_image'))

    # Get category information from product json
    path = os.path.join(settings.BASE_DIR, 'data')

    file_name = "products.json"
    json_url = "%s/%s" % (path, file_name)
    items = json.load(open(json_url))
    category_detail = None
    
    for item in items:
        if item['url'] == ('/' + slug):
            category_detail = item

    context = {
        'products': products,
        'category': related_model._meta.verbose_name_plural.title(),
        'detail': category_detail
    }

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

