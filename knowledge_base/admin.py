from django.contrib import admin
from .models import TechnicalGuide, CaseStudy, Media, MediaRelation
from django.contrib.contenttypes.admin import GenericTabularInline
from tinymce.widgets import TinyMCE
from django.utils.html import format_html

class ImageInline(GenericTabularInline):  # You can also use admin.StackedInline for a different layout
    model = MediaRelation
    extra = 1  # By default, provide 1 empty form

# Refactor these two in KBBaseAdmin
# https://chatgpt.com/share/681878cc-7294-800b-881f-aa305b6ca218
class TechnicalGuideAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    filter_horizontal = ('products',)
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = (
        'content__icontains',                        # exact match or prefix match
        'title__icontains',             # title contains …
    )
    search_help_text = (
        "Search by product title or content."
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('content'):
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30})
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def get_changeform_initial_data(self, request):
        return {'author': request.user.pk}

class CaseStudyAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    filter_horizontal = ('products',)
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = (
        'content__icontains',                        # exact match or prefix match
        'title__icontains',             # title contains …
    )
    search_help_text = (
        "Search by product title or content."
    )
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('project_description', 'challenges', 'solution'):
            kwargs['widget'] = TinyMCE(attrs={'cols': 80, 'rows': 30})
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def get_changeform_initial_data(self, request):
        return {'author': request.user.pk}

class MediaAdmin(admin.ModelAdmin):
    search_fields = ("file", "description", "comment")
    
    def file_name(self, obj):
        # Just call the model’s __str__ method
        return str(obj)

    def thumbnail(self, obj):
        return format_html('<img src="{}" style="max-width:60px; max-height:60px"/>'.format(obj.file.url))
    
    thumbnail.short_description = 'Thumbnail'
    list_display = ['file_name', 'thumbnail',]

admin.site.register(TechnicalGuide, TechnicalGuideAdmin)
admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(Media, MediaAdmin)
