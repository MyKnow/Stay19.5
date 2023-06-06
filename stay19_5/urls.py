"""
URL configuration for stay19_5 project.

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


from stay import views
from stay.views import upload_image

import stay.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', stay.views.main, name='main'),
    path('login/', stay.views.login, name='login'),
    path('info/', stay.views.info, name='info'),
    path('oauth/redirect/', stay.views.getcode, name='oauth'),

    path('map/', stay.views.map, name='map'),
    
    path('upload/', stay.views.index, name = 'index'),
    path('tjdnjsgudqkqh/', upload_image, name='upload_image'),

    path('gallery/', stay.views.gallery, name='gallery'),
    path('photo/', stay.views.photo, name='photo'),
    path('photo/ai', stay.views.photo, name='ai photo'),
    path('get_image_urls', views.get_image_urls, name='get_image_urls'),
    path('gallery_ai/', stay.views.ai_gallery, name='gallery_ai'),
    path('photo/<int:image_id>/', stay.views.image_detail, name='image_detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)