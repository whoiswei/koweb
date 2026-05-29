from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectModule
import json

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('dashboard')
        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('dashboard')
        
    return render(request, 'mainapp/home.html', {
        'login_form': login_form,
        'register_form': register_form
    })

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    return render(request, 'mainapp/dashboard.html')

@login_required
def creator_list(request):
    projects = Project.objects.filter(creator=request.user)
    return render(request, 'mainapp/creator_list.html', {'projects': projects})

@login_required
def creator_form(request, project_id=None):
    if project_id:
        project = get_object_or_404(Project, id=project_id, creator=request.user)
    else:
        project = None

    if request.method == 'POST':
        title = request.POST.get('title')
        story_intro = request.POST.get('story_intro')
        
        if not project:
            project = Project.objects.create(creator=request.user, title=title, story_intro=story_intro)
        else:
            project.title = title
            project.story_intro = story_intro
            project.save()
            
        modules_data = request.POST.get('modules_data', '[]')
        try:
            modules = json.loads(modules_data)
            project.modules.all().delete()
            for idx, mod in enumerate(modules):
                ProjectModule.objects.create(
                    project=project,
                    module_type=mod['module_type'],
                    order=idx,
                    time_limit=mod.get('time_limit', 60),
                    story_text=mod.get('story_text', ''),
                    config_data=mod.get('config_data', {})
                )
        except Exception as e:
            pass
            
        return redirect('creator_list')
        
    return render(request, 'mainapp/creator_form.html', {'project': project, 'module_choices': ProjectModule.MODULE_CHOICES})

@login_required
def creator_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id, creator=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('creator_list')
    return render(request, 'mainapp/creator_confirm_delete.html', {'project': project})

@login_required
def player_list(request):
    projects = Project.objects.all()
    return render(request, 'mainapp/player_list.html', {'projects': projects})

@login_required
def player_play(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'mainapp/player_play.html', {'project': project})