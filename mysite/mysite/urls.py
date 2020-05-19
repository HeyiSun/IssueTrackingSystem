"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from issuetracker import views as issuetracker_views


urlpatterns = [
    path('index/', issuetracker_views.index, name='index'),

    path('login/', issuetracker_views.login, name='login'),
    path('logout/', issuetracker_views.logout, name='logout'),
    path('user/', issuetracker_views.user, name='user'),
    path('project_display/', issuetracker_views.projectDisplay, name='project_display'),
    path('project/', issuetracker_views.projectInfo, name='project_info'),
    path('issue/', issuetracker_views.issueInfo, name='issue_info'),
    path('assign/', issuetracker_views.issueAssign, name='assign'),
    path('lead/', issuetracker_views.leaderAdd, name='lead'),
    path('status_change/', issuetracker_views.statusChange, name='status'),
    path('user_add/', issuetracker_views.userAdd, name='user_add'),
    path('project_add/', issuetracker_views.projectAdd, name='project_add'),
    path('issue_add/', issuetracker_views.issueAdd, name='issue_add'),
    path('status_add/', issuetracker_views.statusAdd, name='status_add'),
    path('statustrans_add/', issuetracker_views.statustransAdd, name='statustrans_add'),

    path('debug/', issuetracker_views.debug, name='debug')
]
