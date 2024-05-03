"""
URL configuration for mabelledjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from core import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.create_npk_object, name='create_npk_object'),
    path('create_npk_object/', views.create_npk_object, name='create_npk_object'),
    path('run_inferrence/', views.run_inferrence, name='run_inferrence'),
]

admin.site.site_header = "MABELLE"
admin.site.site_title = "MABELLE ADMINISTRATION"
admin.site.index_title = "ADMINISTARTION"

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)