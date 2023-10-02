from django.contrib import admin
from .models import TechnicalGuide, CaseStudy, ContentImage, TechnicalGuideImage, CaseStudyImage

class TechnicalGuideImageInline(admin.TabularInline):  # You can also use admin.StackedInline for a different layout
    model = TechnicalGuideImage
    extra = 1  # By default, provide 1 empty form

class TechnicalGuideAdmin(admin.ModelAdmin):
    inlines = [TechnicalGuideImageInline]

class CaseStudyImageInline(admin.TabularInline):
    model = CaseStudyImage
    extra = 1

class CaseStudyAdmin(admin.ModelAdmin):
    inlines = [CaseStudyImageInline]

admin.site.register(TechnicalGuide, TechnicalGuideAdmin)
admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(ContentImage)
