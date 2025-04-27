from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Project, Task
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'tasks/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    return render(request, 'tasks/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def project_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        project = Project.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            owner=request.user
        )
        messages.success(request, 'Проект успешно создан!')
        return redirect('tasks:project_detail', pk=project.pk)
    return render(request, 'tasks/project_form.html')

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        project.start_date = request.POST.get('start_date')
        project.end_date = request.POST.get('end_date')
        project.save()
        messages.success(request, 'Проект успешно обновлен!')
        return redirect('tasks:project_detail', pk=project.pk)
    return render(request, 'tasks/project_form.html', {'project': project})

@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    users = User.objects.all()
    if request.method == 'POST':
        task = Task.objects.create(
            project=project,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            deadline=request.POST.get('deadline'),
            assigned_to_id=request.POST.get('assigned_to')
        )
        messages.success(request, 'Задача успешно создана!')
        return redirect('tasks:project_detail', pk=project_pk)
    return render(request, 'tasks/task_form.html', {'project': project, 'users': users})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    users = User.objects.all()
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.deadline = request.POST.get('deadline')
        task.assigned_to_id = request.POST.get('assigned_to')
        task.save()
        messages.success(request, 'Задача успешно обновлена!')
        return redirect('tasks:project_detail', pk=task.project.pk)
    return render(request, 'tasks/task_form.html', {'task': task, 'project': task.project, 'users': users})

@login_required
def update_task_status(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        task.status = request.POST.get('status')
        task.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def project_delete(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        if project.owner == request.user:
            project.delete()
            messages.success(request, 'Проект успешно удален!')
        else:
            messages.error(request, 'У вас нет прав для удаления этого проекта!')
    return redirect('tasks:project_list')
