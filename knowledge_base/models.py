from django.db import models
from django.template.defaultfilters import slugify
from storage_backends import PublicMediaStorage
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Functions for the image upload paths
def universal_image_upload_path(instance, filename):
    return f"content_images/{filename}"

class ContentImage(models.Model):
    file = models.ImageField(upload_to=universal_image_upload_path, storage=PublicMediaStorage())  # default path
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        # return f"Image {self.id}"
        return self.file.name.split("/")[-1]

class ModelImageRelation(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    image = models.ForeignKey(ContentImage, on_delete=models.CASCADE)
    is_main_image = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.is_main_image:
            # Unset other main images for the related object (CaseStudy, TechnicalGuide, etc.)
            ModelImageRelation.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id
            ).exclude(id=self.id).update(is_main_image=False)
        super().save(*args, **kwargs)

class TechnicalGuide(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    images = GenericRelation(ModelImageRelation)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class CaseStudy(models.Model):
    title = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, default='')
    project_description = models.TextField(blank=True, verbose_name="The Project")
    challenges = models.TextField(blank=True)
    solution = models.TextField(blank=True, verbose_name="Our Solution")
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    images = GenericRelation(ModelImageRelation)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(CaseStudy, self).save(*args, **kwargs)

    def __str__(self):
        return self.title