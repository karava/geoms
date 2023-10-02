from django.urls import path
from .views import TechnicalGuideDetailView, TechnicalGuideListView, CaseStudyDetailView, CaseStudyListView

urlpatterns = [
    path('technical-guides/', TechnicalGuideListView.as_view(), name='technical_guide_list'),
    path('case-studies/', CaseStudyListView.as_view(), name='case_study_list'),
    path('case-studies/<slug:case_study_slug>/', CaseStudyDetailView.as_view(), name='case_study_detail'),
    path('technical-guides/<slug:guide_slug>/', TechnicalGuideDetailView.as_view(), name='technical_guide_detail'),
]