from django.contrib.sitemaps.views import sitemap
from django.urls import path,include
from blog.sitemaps import PostSitemap
from django.contrib import admin
from blog import views as myapp_views
from django.conf.urls import handler404, handler500

sitemaps = {
    'static': PostSitemap,
}

urlpatterns = [
    path('blog/', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

handler404 = myapp_views.error_404
handler500 = myapp_views.error_500
