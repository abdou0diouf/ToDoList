from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q

from .models import Project, Task
from .forms import ProjectForm, TaskForm


@login_required
def dashboard(request):

    query = request.GET.get("q")


    projects = Project.objects.filter(
      owner=request.user
     )


    if query:

     projects = projects.filter(
        Q(name__icontains=query)
        |
        Q(description__icontains=query)
        |
        Q(tasks__title__icontains=query)
    ).distinct()

    total_projects = projects.count()

    tasks = Task.objects.filter(
        project__owner=request.user
    )

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        completed=True
    ).count()

    late_tasks = tasks.filter(
        deadline__lt=timezone.now().date(),
        completed=False
    ).count()


    for project in projects:

        project_tasks = project.tasks.all()

        total = project_tasks.count()

        completed = project_tasks.filter(
            completed=True
        ).count()


        if total > 0:
            project.progress = int(
                (completed / total) * 100
            )
        else:
            project.progress = 0


        project.total_tasks = total
        project.completed_tasks = completed


    return render(
        request,
        "projects/dashboard.html",
        {
            "projects": projects,
            "total_projects": total_projects,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "late_tasks": late_tasks,
        }
    )


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            return redirect("projects:dashboard")
    else:
        form = ProjectForm()

    return render(
        request,
        "projects/create_project.html",
        {"form": form},
    )



@login_required
def toggle_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        project__owner=request.user
    )

    task.completed = not task.completed
    task.save()

    return redirect(
        "projects:project_detail",
        project_id=task.project.id
    )
@login_required
def delete_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        project__owner=request.user
    )

    if request.method == "POST":

        project_id = task.project.id

        task.delete()

        return redirect(
            "projects:project_detail",
            project_id=project_id
        )

    return redirect(
        "projects:project_detail",
        project_id=task.project.id
    )
@login_required
def edit_task(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        project__owner=request.user
    )

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():
            form.save()

            return redirect(
                "projects:project_detail",
                project_id=task.project.id
            )

    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "projects/edit_task.html",
        {
            "form": form,
            "task": task,
        }
    )

@login_required
def project_detail(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )


    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)
            task.project = project
            task.save()

            return redirect(
                "projects:project_detail",
                project_id=project.id
            )

    else:

        form = TaskForm()



    # Toutes les tâches du projet
    all_tasks = project.tasks.all()


    # Calcul réel de progression
    total_tasks = all_tasks.count()


    completed_tasks = all_tasks.filter(
        completed=True
    ).count()



    if total_tasks > 0:

        progress = int(
            (completed_tasks / total_tasks) * 100
        )

    else:

        progress = 0



    # Filtre affichage
    status = request.GET.get("status")


    tasks = all_tasks


    if status == "completed":

        tasks = tasks.filter(
            completed=True
        )


    elif status == "pending":

        tasks = tasks.filter(
            completed=False
        )



    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
            "tasks": tasks,
            "form": form,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "progress": progress,
            "today": timezone.now().date(),
        },
    )
@login_required
def delete_project(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    if request.method == "POST":

        project.delete()

        return redirect(
            "projects:dashboard"
        )

    return redirect(
        "projects:dashboard"
    )
 
@login_required
def profile(request):

    projects_count = Project.objects.filter(
        owner=request.user
    ).count()


    tasks_count = Task.objects.filter(
        project__owner=request.user,
        completed=True
    ).count()


    return render(
        request,
        "projects/profile.html",
        {
            "projects_count": projects_count,
            "tasks_count": tasks_count,
            "date_joined": request.user.date_joined,
        }
    )