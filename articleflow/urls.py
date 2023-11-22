from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blogapp.sitemap import CategorySitemap, PostSitemap
from blogapp.views import robots_txt


sitemaps = {
    'post': PostSitemap,
    'category': CategorySitemap,
    # Add more sitemaps if needed
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# to handle page not found 404
handler404 = 'blogapp.views.custom_404_page'
