from django.shortcuts import get_object_or_404, render
from .models import TechnicalGuide, CaseStudy
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class TechnicalGuideListView(ListView):
    model = TechnicalGuide
    template_name = 'technical_guide_list.html'
    context_object_name = 'guides'
    paginate_by = 10    # default items per page
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        new_context = []
        
        for item in context['guides']:
            main_image = item.images.filter(is_main_image=True).first()
            new_context.append({
                'title': item.title,
                'created_at': item.created_at,
                'content': item.content,
                'slug': item.slug,
                'thumbnail': main_image.image.file.url if main_image else None
            })

        context['guides'] = new_context
        context['page_title'] = 'Technical Guides'

        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('pagesize', self.paginate_by)

    def get_queryset(self):
        queryset = super().get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(queryset, self.get_paginate_by(queryset))

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return queryset

class CaseStudyListView(ListView):
    model = CaseStudy
    template_name = 'case_study_list.html'
    context_object_name = 'studies'
    paginate_by = 10    # default items per page

    def get_paginate_by(self, queryset):
        return self.request.GET.get('pagesize', self.paginate_by)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(queryset, self.get_paginate_by(queryset))

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        new_context = []
        
        for item in context['studies']:
            main_image = item.images.filter(is_main_image=True).first()
            new_context.append({
                'title': item.title,
                'caption': item.caption,
                'description': item.project_description,
                'slug': item.slug,
                'thumbnail': main_image.image.file.url if main_image else None
            })

        context['studies'] = new_context
        context['page_title'] = 'Case Studies'

        return context

class CaseStudyDetailView(DetailView):
    model = CaseStudy
    template_name = 'case_study_detail.html'
    context_object_name = 'study'
    slug_url_kwarg = 'case_study_slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_image'] = self.object.images.filter(is_main_image=True).first()
        gallery_image_items = self.object.images.filter(is_main_image=False)
        gallery_images = []
        for item in gallery_image_items:
            gallery_images.append(item.image.file.url)
        context['gallery_images'] = gallery_images
        context['page_title'] = self.object.title
        return context

class TechnicalGuideDetailView(DetailView):
    model = TechnicalGuide
    template_name = 'technical_guide_detail.html'
    context_object_name = 'guide'
    slug_url_kwarg = 'guide_slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_image'] = self.object.images.filter(is_main_image=True).first()
        context['page_title'] = self.object.title
        return context