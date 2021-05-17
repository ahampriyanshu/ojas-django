from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from blog.sitemaps import PostSitemap
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


handler404 = 'blog.views.error_404'
handler500 = 'blog.views.error_500'
handler403 = 'blog.views.error_403'
handler400 = 'blog.views.error_400'


sitemaps = {
    'static': PostSitemap,
}


urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
