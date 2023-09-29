from django.urls import path
from . import views

urlpatterns = [
    path('technical-guides/', views.technical_guide_list, name='technical_guide_list'),
    path('case-studies/', views.case_study_list, name='case_study_list'),
]