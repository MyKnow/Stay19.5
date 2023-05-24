"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import common.views
import map.views
import qr.views
import gallery.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', common.views.main, name='main'),
    path('login/', common.views.login, name='login'),
    path('info/', common.views.info, name='info'),

    path('map/', map.views.map, name='map'),

    path('upload/', qr.views.upload, name='upload'),

    path('gallery/', gallery.views.gallery, name='gallery'),
    path('photo/', gallery.views.photo, name='photo'),
    path('gallery/ai', gallery.views.ai_gallery, name='ai gallery'),
    path('photo/ai', gallery.views.photo, name='ai photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
