"""trashcash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from points import views as core_views

urlpatterns = [
    url(r'^$', core_views.home, name="testhome"),

    url(r'^login/$', auth_views.login, name="login"),

    url(r'^logout/$', auth_views.logout, {'next_page': '/home'}, name="logout"),
    
    url(r'^admin/', admin.site.urls, name="admin"),

    url(r'^signup/$', core_views.signup, name='signup'),

    url(r'^home/$', core_views.home, name="home"),

    url(r'^users/$', core_views.admin_view_users, name="admin_users"),

    url(r'^trash_submissions/new$', core_views.admin_trash_submission, name='trash_submission'),

    url(r'^create_new_admin/$', core_views.admin_new, name="new_admin"),

]
