from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "projects/new/",
        views.create_project,
        name="create_project",
    ),

    path(
        "project/<int:project_id>/",
        views.project_detail,
        name="project_detail",
    ),
    path(
    "task/<int:task_id>/toggle/",
    views.toggle_task,
    name="toggle_task",
    ),
    path(
    "task/<int:task_id>/delete/",
    views.delete_task,
    name="delete_task",
    ),
    path(
    "task/<int:task_id>/edit/",
    views.edit_task,
    name="edit_task",
    ),
    path(
    "project/<int:project_id>/delete/",
    views.delete_project,
    name="delete_project"
    ),
    path(
    "profile/",
    views.profile,
    name="profile"
    ),
    
]