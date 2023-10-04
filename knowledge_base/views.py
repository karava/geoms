from django.shortcuts import get_object_or_404, render
from .models import TechnicalGuide, CaseStudy
from django.views.generic import ListView, DetailView

class TechnicalGuideListView(ListView):
    model = TechnicalGuide
    template_name = 'technical_guide_list.html'
    context_object_name = 'guides'

class CaseStudyListView(ListView):
    model = CaseStudy
    template_name = 'case_study_list.html'
    context_object_name = 'studies'
    
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
                'thumbnail': main_image.image.file.name if main_image else None
            })

        context['studies'] = new_context

        return context

class CaseStudyDetailView(DetailView):
    model = CaseStudy
    template_name = 'case_study_detail.html'
    context_object_name = 'study'
    slug_url_kwarg = 'case_study_slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_image'] = self.object.images.filter(is_main_image=True).first()
        return context

class TechnicalGuideDetailView(DetailView):
    model = TechnicalGuide
    template_name = 'technical_guide_detail.html'
    context_object_name = 'guide'
    slug_url_kwarg = 'guide_slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_image'] = self.object.images.filter(is_main_image=True).first()
        return context