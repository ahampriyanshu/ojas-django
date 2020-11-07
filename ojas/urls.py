from django.contrib.sitemaps.views import sitemap
from django.urls import path,include
from blog.sitemaps import PostSitemap
from django.contrib import admin

sitemaps = {
    'static': PostSitemap,
}

urlpatterns = [
    path('blog/', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]
