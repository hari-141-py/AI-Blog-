# blog_generator/urls.py

from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog_generator'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_register/', views.user_register, name='user_register'),
    path('all_blogs/', views.all_blogs, name='all_blogs'),
    path('generate_blog/', views.generate_blog, name='generate_blog'),
    path('verify/<str:token>/', views.verify, name='verify'),
    path('howTo/', views.index, name='index'),
    path('Vibe/', views.index, name='index'),
    path('connect/', views.index, name='index'),
    path('blog_details/<int:i>/', views.blog_details, name='blog_details'),
    # Catch-all pattern to redirect to custom 404 page
    re_path(r'^.*$', views.custom_404),
]

if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)