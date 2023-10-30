import os, json
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import BaseProduct, Geocell, Geogrid, Geotextile, GCL, DrainageProduct, ProductModelImageRelation
from django.db.models import Prefetch
from .forms import ProductEnquiryForm
from django.core.mail import send_mail

# Create your views here.

# This views lists an overview of the generic categories
def index(request):
    path = os.path.join(settings.BASE_DIR, 'data')

    file_name = "products.json"
    json_url = "%s/%s" % (path, file_name)
    items = json.load(open(json_url))

    context = {'categories': items, 'page_title': 'Product Categories'}
    return render(request, 'index.html', context)

def CategoryListView(request, slug):
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
    default_image = ProductModelImageRelation.objects.filter(is_default=True)
    products = products.prefetch_related(Prefetch('images', queryset=default_image, to_attr='default_image'))

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
        'detail': category_detail,
        'page_title': related_model._meta.verbose_name_plural.title()
    }

    return render(request, 'category.html', context)


class ProductDetailView(DetailView):
    model = BaseProduct
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['default_image'] = self.object.images.filter(is_default=True).first()
        context['product_images'] = self.object.images.all()
        context['model_name'] = self.object.get_product_detail_name()
        context['resources'] = self.object.resources.all()
        context['page_title'] = self.object.title

        # Getting the related products
        detail_model = self.object.get_product_detail_model()
        if detail_model:
           related_products = BaseProduct.objects.filter(
            id__in=type(detail_model).objects.exclude(id=detail_model.id).values('baseproduct__id')).exclude(id=self.object.id)  # Exclude the current product
           context['related_products'] = related_products
        else:
            context['related_products'] = BaseProduct.objects.none()
        return context
    
def product_enquiry(request):
    if request.method == 'POST':
        form = ProductEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            
            # Sending email:
            subject = 'New Product Enquiry'
            message = f"""
Name: {enquiry.full_name}
Email: {enquiry.email}
Phone: {enquiry.phone}
Existing Customer: {enquiry.existing_customer}
Product Interested In: {enquiry.product_interested_in}
Estimated Quantity: {enquiry.estimated_quantity}
Specifications: {enquiry.specifications}
Project Based: {enquiry.project_based}
Needed By: {enquiry.needed_by}
"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL, # Sender's email
                ['your_email@example.com'], # Replace with your receiving email
            )

            # Redirect to a 'thank you' page or similar after submission
            return redirect('contact')
    else:
        form = ProductEnquiryForm()
    return render(request, 'contact.html', {'form': form, 'page_title': 'Contact Us'})

