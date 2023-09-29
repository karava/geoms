from django.contrib import admin
from .models import TechnicalGuide, CaseStudy, ContentImage, TechnicalGuideImage

class TechnicalGuideImageInline(admin.TabularInline):  # You can also use admin.StackedInline for a different layout
    model = TechnicalGuideImage
    extra = 1  # By default, provide 1 empty form

class TechnicalGuideAdmin(admin.ModelAdmin):
    inlines = [TechnicalGuideImageInline]

admin.site.register(TechnicalGuide, TechnicalGuideAdmin)
admin.site.register(CaseStudy)
admin.site.register(ContentImage)
