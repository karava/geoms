import os, json
from django.conf import settings
from django.shortcuts import render

# Create your views here.

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

    context = {'data': application, 'page_title': application['title']}
    return render(request, 'application/detail.html', context)
