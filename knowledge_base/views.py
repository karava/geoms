from django.shortcuts import get_object_or_404, render
from .models import TechnicalGuide, CaseStudy

def technical_guide_list(request):
    guides = TechnicalGuide.objects.all()
    return render(request, 'technical_guide_list.html', {'guides': guides})

def case_study_list(request):
    studies = CaseStudy.objects.all()
    return render(request, 'case_study_list.html', {'studies': studies})

def case_study_detail(request, case_study_slug):
    study = get_object_or_404(CaseStudy, slug=case_study_slug)
    return render(request, 'case_study_detail.html', {'study': study})

def technical_guide_detail(request, guide_slug):
    guide = get_object_or_404(TechnicalGuide, slug=guide_slug)
    main_image = guide.images.filter(is_main_image=True).first()
    
    context = {
        'guide': guide,
        'main_image': main_image,
    }
    
    return render(request, 'technical_guide_detail.html', context)