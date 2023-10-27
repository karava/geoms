from django.contrib import admin
from .models import TechnicalGuide, CaseStudy, ContentImage, ModelImageRelation
from django.contrib.contenttypes.admin import GenericTabularInline

class ImageInline(GenericTabularInline):  # You can also use admin.StackedInline for a different layout
    model = ModelImageRelation
    extra = 1  # By default, provide 1 empty form

class TechnicalGuideAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

class CaseStudyAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

admin.site.register(TechnicalGuide, TechnicalGuideAdmin)
admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(ContentImage)
