import os, json
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ProductEnquiryForm
from django.core.mail import send_mail

# Create your views here.
def index(request):
    with open(settings.BASE_DIR / 'data/products.json') as f:
        products = json.load(f)
    
    products_dict = {}
    
    for product in products:
        products_dict[product['title'].lower().replace(' ', '_')] = product
    
    context = {'products': products_dict, 'page_title': 'Infratex'}

    return render(request, 'static_pages/index.html', context)

def render_applications(request):
    path = os.path.join(settings.BASE_DIR, 'data', 'applications')

    applications = []
    for f in os.listdir(path):
        if f.endswith("json"): # select only json
            file_name = f.split('.')[0]
            json_url = "%s/%s" % (path, f)
            item = json.load(open(json_url))
            applications.append({
                'url': file_name,
                'thumbnail': item['thumbnail'],
                'title': item['title'],
                'description': item['What_is_text']
            })

    context = {'applications': applications, 'page_title': 'Applications'}
    return render(request, 'application/index.html', context)

def render_application_detail(request, slug):
    path = os.path.join(settings.BASE_DIR, 'data', 'applications')
    json_url = "%s/%s.json" % (path, slug)
    application = json.load(open(json_url))

    product_urls = {
        "View InfraThread": reverse('products:product_category', kwargs={'category_slug': 'geotextiles'}),
        "View InfraSheet": reverse('products:product_category', kwargs={'category_slug': 'drainage-systems'}),
        "View InfraStrip": reverse('products:product_category', kwargs={'category_slug': 'drainage-systems'}),
        "View InfraGrid": reverse('products:product_category', kwargs={'category_slug': 'geogrids'}),   
        "View InfraCell": reverse('products:product_category', kwargs={'category_slug': 'geocells'}),
        "View InfraDrain": reverse('products:product_category', kwargs={'category_slug': 'drainage-systems'}),
        "View InfraClay": reverse('products:product_category', kwargs={'category_slug': 'gcls'}),
    }

    # Iterate over the links and update the URLs
    for product_application in application.get('Product_applications', []):
        for link in product_application.get('link', []):
            if link["label"] in product_urls:
                link["url"] = product_urls[link["label"]]

    context = {
        'data': application, 
        'page_title': application['title'],
        'meta_description': application['Summary_text']
        }
    return render(request, 'application/detail.html', context)

def product_enquiry(request):
    if request.method == 'POST':
        form = ProductEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            
            # Sending email:
            subject = 'New Product Enquiry - Infratex'
            message = f"""
Name: {enquiry.full_name}
Company: {enquiry.company}
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
                ['support@geosynthetics.net.au'], # Replace with your receiving email
            )

            # Redirect to a 'thank you' page or similar after submission
            return redirect('contact')
    else:
        product = request.GET.get('product')
        form = ProductEnquiryForm()
    return render(request, 'static_pages/contact.html', {'form': form, 'page_title': 'Contact Us', 'product':product})