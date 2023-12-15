from django.db import models
from django.template.defaultfilters import slugify
from storage_backends import PublicMediaStorage
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import SuspiciousFileOperation
from storage_backends import PublicMediaStorage
from django.conf import settings

# Functions for the image upload paths
def universal_image_upload_path(instance, filename):
    return f"{settings.MEDIA_FOLDER_NAME}/{filename}"

class Media(models.Model):
    file = models.FileField(upload_to=universal_image_upload_path, storage=PublicMediaStorage())  # default path
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        # return f"Image {self.id}"
        return self.file.name.split("/")[-1]
    
    class Meta:
        verbose_name_plural = "Media"
    
    def delete(self, *args, **kwargs):
        # Check if there's a file associated with this instance
        if self.file:
            # Call the storage's delete method
            self.file.storage.delete(self.file.name)
        super().delete(*args, **kwargs)

@receiver(pre_save, sender=Media)
def media_file_pre_save(sender, instance, **kwargs):
    if instance.file:
        storage = PublicMediaStorage()

        # Construct the full file path
        file_path = f"{settings.MEDIA_FOLDER_NAME}/{instance.file.name}"

        # Check if a file with the same name exists
        file_exists = storage.exists(file_path)

        if not instance.file._committed and file_exists:
            raise SuspiciousFileOperation(f"A file with name '{file_path}' already exists.")

class MediaRelation(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    media_type = models.CharField(max_length=10, choices=(('image', 'Image'), ('document', 'Document')), default='image')
    
    image = models.ForeignKey(Media, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.is_default:
            # Unset other main images for the related object (CaseStudy, TechnicalGuide, etc.)
            MediaRelation.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id
            ).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        # Get the related object's class name to determine the type
        related_object_type = self.content_type.model_class().__name__

        # Access the 'title' attribute for TechnicalGuide and CaseStudy
        if related_object_type in ['TechnicalGuide', 'CaseStudy']:
            title = getattr(self.content_object, 'title', 'Unknown')
            return f"{self.media_type} for {related_object_type} '{title}' (Order: {self.order})"

        # Fallback for any other types
        return f"{self.media_type} related to {related_object_type} (ID: {self.object_id})"

class TechnicalGuide(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    images = GenericRelation(MediaRelation)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class CaseStudy(models.Model):
    title = models.CharField(max_length=255)
    caption = models.CharField(max_length=255, default='')
    project_description = models.TextField(blank=True, verbose_name="The Project")
    challenges = models.TextField(blank=True)
    solution = models.TextField(blank=True, verbose_name="Our Solution")
    slug = models.SlugField(unique=True, blank=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    images = GenericRelation(MediaRelation)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super(CaseStudy, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Case Studies"