from django.conf.urls import url
from django.urls import path,include
from . import views
from .feeds import LatestPostsFeed
from .views import search, PostViewSet
from rest_framework import routers 


router = routers.DefaultRouter() 
router.register(r'api', PostViewSet) 


app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    url(r'^blog/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact_page'),
    url(r'^author/(?P<post_author>[-\w]+)/$',views.post_author, name='post_author'),
    path('search', search, name='search'),
    path('', include(router.urls)), 
    path('api-auth/', include('rest_framework.urls')),
]