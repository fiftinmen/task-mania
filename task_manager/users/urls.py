"""
URL configuration for task_manager project.

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

from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


urlpatterns = [
    path("", views.UsersIndexView.as_view(), name="users_index"),
    path("<int:pk>/", views.UsersDetailView.as_view(), name="users_detail"),
    path("create/", views.UsersCreateView.as_view(), name="users_create"),
    path("login/", views.UsersLoginView.as_view(), name="users_login"),
    path("logout/", views.UsersLogoutView.as_view(), name="users_logout"),
    path("profile/", views.UsersDetailView.as_view(), name="users_profile"),
    path(
        "delete/<int:pk>/",
        login_required(views.UsersDeleteView.as_view()),
        name="users_delete",
    ),
    path(
        "update/<int:pk>/",
        login_required(views.UsersUpdateView.as_view()),
        name="users_update",
    ),
]
