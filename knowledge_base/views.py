from django.shortcuts import render
from .models import TechnicalGuide, CaseStudy

def technical_guide_list(request):
    guides = TechnicalGuide.objects.all()
    return render(request, 'technical_guide_list.html', {'guides': guides})

def case_study_list(request):
    studies = CaseStudy.objects.all()
    return render(request, 'case_study_list.html', {'studies': studies})
