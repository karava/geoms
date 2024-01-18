import os, json
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import Product, ProductMediaRelation
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

# Create your views here.

# This views lists an overview of the generic categories
def index(request):
    path = os.path.join(settings.BASE_DIR, 'data')

    file_name = "products.json"
    json_url = "%s/%s" % (path, file_name)
    items = json.load(open(json_url))

    context = {'categories': items, 'page_title': 'Product Categories'}
    return render(request, 'index.html', context)

def CategoryListView(request, category_slug):
    # Mapping slugs to their corresponding categories
    slug_to_category = {
        'geocells': 'geocell',
        'gcls': 'gcl',
        'geotextiles': 'geotextile',
        'geogrids': 'geogrid',
        'drainage-systems': 'drainage',
    }

    # Check if the provided slug is valid
    if category_slug not in slug_to_category:
        # Handle invalid slugs (you can render an error page or raise a 404)
        return render(request, 'error_page.html', {'message': 'Invalid category.'})
    
    category = slug_to_category[category_slug]

    # Get all the products in the category
    products = Product.objects.filter(category=category)

    # Prefetch related default images
    default_image = ProductMediaRelation.objects.filter(is_default=True, resource_type='product_image')
    products = products.prefetch_related(Prefetch('media', queryset=default_image, to_attr='default_image'))

    # Get category information from product json
    path = os.path.join(settings.BASE_DIR, 'data')

    file_name = "products.json"
    json_url = "%s/%s" % (path, file_name)
    items = json.load(open(json_url))
    category_detail = None
    
    for item in items:
        if item['url'] == ('/' + category_slug):
            category_detail = item

    context = {
        'products': products,
        'category': category_slug.title().replace('_', ' '),
        'category_slug': category_slug,
        'detail': category_detail,
        'page_title': category_slug.title().replace('_', ' ')
    }

    return render(request, 'category_list.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        # Use the product_code from the URL to get the product
        product_code = self.kwargs.get('product_code')
        return get_object_or_404(Product, code=product_code)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['default_image'] = self.object.media.filter(is_default=True, resource_type='product_image').first()
        context['product_images'] = self.object.media.filter(resource_type='product_image').all()
        context['resources'] = self.object.media.exclude(resource_type='product_image').all()
        context['page_title'] = self.object.title

        # Getting the related products based on category
        related_products = Product.objects.filter(category=self.object.category).exclude(id=self.object.id)
        context['related_products'] = related_products
        context['category_slug'] = self.kwargs.get('category_slug')
        
        return context

