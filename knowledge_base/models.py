import os
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
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

    alt_text = models.CharField(max_length=255, blank=True, null=True, help_text="Alternative text for SEO and accessibility.")
    
    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.is_default:
            # Unset other main images for the related object (CaseStudy, TechnicalGuide, etc.)
            MediaRelation.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id
            ).exclude(id=self.id).update(is_default=False)
        if not self.alt_text and self.image and self.image.file and self.image.file.name:
            # Extract file name, remove extension, replace underscores
            base_name = os.path.basename(self.image.file.name)      # e.g. "my_image_file.jpg"
            base, ext = os.path.splitext(base_name)                 # base="my_image_file", ext=".jpg"
            base = base.replace("_", " ")                           # "my image file"
            self.alt_text = base
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
    products = models.ManyToManyField(
        'products.Product',
        related_name='technical_guides',
        blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,              # allow data migration if older rows exist
        blank=True,             # optional so admin can auto-set
        related_name='technical_guides',
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("knowledge_base:technical_guide_detail", kwargs={"guide_slug": self.slug})

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
    products = models.ManyToManyField(
        'products.Product',
        related_name='case_studies',
        blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,              # allow data migration if older rows exist
        blank=True,             # optional so admin can auto-set
        related_name='case_studies',
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super(CaseStudy, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Case Studies"

    def get_absolute_url(self):
        return reverse("knowledge_base:case_study_detail", kwargs={"case_study_slug": self.slug})