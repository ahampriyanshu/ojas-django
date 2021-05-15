from django.conf.urls import url
from django.urls import path,include
from . import views
from .feeds import LatestPostsFeed
from .views import search, PostViewSet
from rest_framework import routers 
from django.views.generic import TemplateView
import captcha

router = routers.DefaultRouter() 
router.register(r'api', PostViewSet) 


app_name = 'blog'
urlpatterns = [
    path('', views.most_viewed, name='most_viewed'),
    path('contact/', views.contact_page, name='contact_page'),
    path('articles/', views.post_list, name='post_list'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe/confirm/', views.subscription_confirmation, name='subscription_confirmation'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    url(r'^blog/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'),
    path('preview/<int:id>/', views.preview, name = "preview"),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('about/', views.about_page, name='about'),
    path('author/<str:post_author>/', views.post_author, name = "post_author"),
    path('search', search, name='search'),
    path('me/', views.me, name='me'),
    path('', include(router.urls)),
    path('captcha/', include('captcha.urls')), 
    path('api-auth/', include('rest_framework.urls')),
    path('offline/', views.offline, name='offline'),
    path('sw.js', views.ServiceWorkerView.as_view(), name=views.ServiceWorkerView.name,),
]