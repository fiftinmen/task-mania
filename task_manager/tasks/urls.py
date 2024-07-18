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

from django.urls import path
from . import views


urlpatterns = [
    path("", views.TasksIndexView.as_view(), name="tasks_index"),
    path("create/", views.TasksCreateView.as_view(), name="tasks_create"),
    path(
        "delete/<int:pk>/",
        views.TasksDeleteView.as_view(),
        name="tasks_delete",
    ),
    path(
        "update/<int:pk>/",
        views.TasksUpdateView.as_view(),
        name="tasks_update",
    ),
]
