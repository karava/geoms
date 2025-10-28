import os, json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from .models import Product, ProductMediaRelation
from knowledge_base.models import TechnicalGuide, CaseStudy
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
    # Redirect singular URLs to canonical plural forms with 301 redirect
    # This ensures we don't have duplicate content for SEO
    singular_to_plural_redirects = {
        'geocell': 'geocells',
        'gcl': 'gcls',
        'geotextile': 'geotextiles',
        'geogrid': 'geogrids',
        'drainage-systems': 'drainage',  # Legacy URL redirect
    }

    # If it's a singular URL or legacy URL, redirect to canonical plural form
    if category_slug in singular_to_plural_redirects:
        return redirect('products:product_category',
                       category_slug=singular_to_plural_redirects[category_slug],
                       permanent=True)

    # Map plural URLs to database category values
    # Database stores singular (Django convention), URLs use plural (better for SEO)
    plural_url_to_db_category = {
        'geocells': 'geocell',
        'gcls': 'gcl',
        'geotextiles': 'geotextile',
        'geogrids': 'geogrid',
        'drainage': 'drainage',  # This one stays singular (sounds better)
    }

    # Check if the category is valid
    if category_slug not in plural_url_to_db_category:
        # Handle invalid slugs - return 404
        from django.http import Http404
        raise Http404(f"Category '{category_slug}' not found")

    # Get the database category value
    db_category = plural_url_to_db_category[category_slug]

    # Get all the products in the category
    products = Product.objects.filter(category=db_category)

    # Prefetch related default images
    default_image = ProductMediaRelation.objects.filter(is_default=True, resource_type='product_image')
    products = products.prefetch_related(Prefetch('media', queryset=default_image, to_attr='default_image'))

    # Get category information from product json
    path = os.path.join(settings.BASE_DIR, 'data')

    file_name = "products.json"
    json_url = "%s/%s" % (path, file_name)
    items = json.load(open(json_url))
    category_detail = None

    # Use db_category to find the right item in products.json
    # (products.json uses singular forms like "/geocell")
    for item in items:
        if item['url'] == ('/' + db_category):
            category_detail = item

    context = {
        'products': products,
        'category': category_slug.title().replace('_', ' '),
        'category_slug': category_slug,  # Keep plural for templates/URLs
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
        context['meta_description'] = self.object.short_description
        context['model_name'] = self.object.category.title().replace('_', ' ')

        # Getting the related products based on category
        related_products = Product.objects.filter(category=self.object.category).exclude(id=self.object.id)
        context['related_products'] = related_products
        context['category_slug'] = self.kwargs.get('category_slug')

        # Get the knowledge base items
        context['technical_guides'] = self.object.technical_guides.all()
        context['case_studies'] = self.object.case_studies.all()
        context["guides_and_studies_total"] = context["technical_guides"].count() + context["case_studies"].count()
        
        return context

class ProductSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        products = Product.objects.filter(title__icontains=query)[:10]  # limit to 10 results

        # Prepare data to return as JSON
        # Typically you might return just a list of names or some additional fields
        results = []
        for product in products:
            results.append({
                'id': product.id,
                'title': product.title,
                'url': product.get_absolute_url()
            })

        # Return a JSON response
        return JsonResponse(results, safe=False)
    
class CombinedSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        products = Product.objects.filter(title__icontains=query)[:10]  # limit to 10 results
        techGuides = TechnicalGuide.objects.filter(title__icontains=query)[:10]
        caseStudies = CaseStudy.objects.filter(title__icontains=query)[:10]

        # Prepare data to return as JSON
        # Typically you might return just a list of names or some additional fields
        results = []
        for product in products:
            results.append({
                'id': product.id,
                'title': product.title,
                'url': product.get_absolute_url()
            })
        
        for guide in techGuides:
            results.append({
                'id': guide.id,
                'title': guide.title,
                'url': guide.get_absolute_url()
            })
        
        for study in caseStudies:
            results.append({
                'id': study.id,
                'title': study.title,
                'url': study.get_absolute_url()
            })

        # Return a JSON response
        return JsonResponse(results, safe=False)