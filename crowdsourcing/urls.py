"""crowdsourcing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from base import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.loginView.as_view(), name='register'),

    path('', views.homeView.as_view(), name='home'),
    path('developer/', views.developerView.as_view(), name="developer"),
    path('register/', views.registerView.as_view(), name="register"),
    path('login/', views.loginView.as_view(), name='login'),

    path('release/', views.releaseView.as_view(), name='release'),
    path('details/', views.details, name='details'),
    path('task/<taskId>', views.task, name='task'),
    path('profile/', views.profileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
    path('jointask/<taskId>', views.jointask, name='jointask'),
    path('mytask/<taskId>', views.mytaskView.as_view(), name='mytask'),
    path('reward/<taskId>', views.rewardView.as_view(), name='reward'),

    path('private/', views.privateView.as_view(), name='private'),
    path('download/', views.download, name='download'),
    path('others/<userId>', views.getuser, name='getuser'),


]
