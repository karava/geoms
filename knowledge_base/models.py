from django.db import models
from django.template.defaultfilters import slugify

# Functions for the image upload paths
def universal_image_upload_path(instance, filename):
    return f"content_images/{filename}"

class ContentImage(models.Model):
    file = models.ImageField(upload_to=universal_image_upload_path)  # default path
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"

class TechnicalGuide(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class TechnicalGuideImage(models.Model):
    technical_guide = models.ForeignKey(TechnicalGuide, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(ContentImage, on_delete=models.CASCADE)
    is_main_image = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.is_main_image:
            # Unset other main images for this TechnicalGuide
            TechnicalGuideImage.objects.filter(technical_guide=self.technical_guide).update(is_main_image=False)
        super().save(*args, **kwargs)

class CaseStudy(models.Model):
    title = models.CharField(max_length=255)
    project_description = models.TextField(blank=True, verbose_name="The Project")
    challenges = models.TextField(blank=True)
    solution = models.TextField(blank=True, verbose_name="Our Solution")
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(CaseStudy, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class CaseStudyImage(models.Model):
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(ContentImage, on_delete=models.CASCADE)
    is_main_image = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.is_main_image:
            # Unset other main images for this CaseStudy
            CaseStudyImage.objects.filter(case_study=self.case_study).update(is_main_image=False)
        super().save(*args, **kwargs)
