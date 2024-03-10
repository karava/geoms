from django.contrib import admin
from .models import TechnicalGuide, CaseStudy, Media, MediaRelation
from django.contrib.contenttypes.admin import GenericTabularInline
from tinymce.widgets import TinyMCE

class ImageInline(GenericTabularInline):  # You can also use admin.StackedInline for a different layout
    model = MediaRelation
    extra = 1  # By default, provide 1 empty form

class TechnicalGuideAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

class CaseStudyAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('project_description', 'challenges', 'solution'):
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30})
        return super().formfield_for_dbfield(db_field, **kwargs)

admin.site.register(TechnicalGuide, TechnicalGuideAdmin)
admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(Media)
