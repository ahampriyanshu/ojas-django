from django.contrib.sitemaps.views import sitemap
from django.urls import path,include
from blog.sitemaps import PostSitemap
from django.contrib import admin
from blog import views as blog
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static


handler404 = blog.error_404
handler500 = blog.error_500


sitemaps = {
    'static': PostSitemap,
}


urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('setup/', include('blog.urls', namespace='setup')),
    path('admin/', admin.site.urls),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)