from django.contrib.sitemaps import Sitemap
from .models import Item
from django.urls import reverse

class ProductSitemap(Sitemap):

    changefreq = 'daily'

    def items(self):
        return Item.objects.all()


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['about_us','Allproducts','contact','category_sarees','tailoring','faqs']

    def location(self, item):
        return reverse('cart:'+ item)
