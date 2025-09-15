"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from routing import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("signup/", include("django.contrib.auth.urls")),
    path("login/", include("django.contrib.auth.urls")),
    path("", include("accounts.urls")),
    path("", include("books.urls")),
    path("about/", views.about, name="about"),
    path("signup/", views.signup, name="signup"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("user_home/", views.user_home, name="user_home"),
    path("profile/", views.profile, name="profile"),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, 
document_root=settings.MEDIA_ROOT) 