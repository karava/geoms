from django.contrib import sitemaps
from django.urls import reverse
import os
from django.conf import settings
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return ["applications", "aboutus", "contact", "capabilities_statement", "products:index"]

    def location(self, item):
        return reverse(item)

class HomeViewSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = "daily"

    def items(self):
        return ["home"]

    def location(self, item):
        return reverse(item)

class CategorySitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # Return the category slugs you want in the sitemap
        return ["geocells", "gcls", "geotextiles", "geogrids", "drainage-systems"]

    def location(self, item):
        # item will be one of the slugs above
        return reverse("products:product_category", kwargs={"category_slug": item})

class ApplicationSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        """ Return a list of valid slugs by scanning the 'data/applications' folder """
        apps_dir = os.path.join(settings.BASE_DIR, 'data', 'applications')
        all_files = os.listdir(apps_dir)
        # Filter down to just .json, strip the .json extension to get the slug
        slugs = [os.path.splitext(filename)[0] for filename in all_files if filename.endswith('.json')]
        return slugs

    def location(self, item):
        """ item is the slug from the folder """
        return reverse('application_detail', kwargs={'slug': item})