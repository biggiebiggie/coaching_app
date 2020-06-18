from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Student, Coach, Tag, Team
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login/')
def index(request):
    print(request)

    if Coach.objects.filter(user = request.user):
        my_teams = Team.objects.filter(coach__user = request.user)
        context = {
            'my_teams': my_teams
        }
        return render(request, 'coaching_app/index.html', context)

    elif Student.objects.filter(user = request.user):
        my_teams = Team.objects.filter(student__user = request.user)
        print(my_teams)
        context = {
            'my_teams': my_teams
        }
        return render(request, 'coaching_app/index.html', context)
    return render(request, 'coaching_app/index.html')

@login_required(login_url='/account/login/')
def team_create(request):
    if request.method== "POST":
        coach = Coach.objects.get(user = request.user)

        team_name = request.POST["team_name"]
        team = Team()
        team.name = team_name
        team.save()
        team.coach.add(coach)
        team.save()

        return redirect('coaching_app:team_view', pk=team.pk)
    return render(request, 'coaching_app/team_create.html')

@login_required(login_url='/account/login/')
def team_view(request, pk):
    team = get_object_or_404(Team, pk=pk)
    
    # Get the coaches and students
    coaches = team.coach.all()
    students = team.student.all()

    if not Coach.objects.get(user = request.user) == None:
        print("this is coach")

    elif not Student.objects.get(user = request.user) == None:
        print("this is student")

    context = {
        'team': team,
        'coaches': coaches,
        'students': students
    }
    return render(request, 'coaching_app/team_view.html', context)

@login_required(login_url='/account/login/')
def team_insert(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if request.method == "POST":
        if 'student_pk' in request.POST:
            student_pk = request.POST["student_pk"]
            student = get_object_or_404(Student, pk=student_pk)
            team.student.add(student)

        elif 'coach_pk' in request.POST:
            coach_pk = request.POST["coach_pk"]
            coach = get_object_or_404(Coach, pk=coach_pk)
            team.coach.add(coach)

    return redirect('coaching_app:team_settings', pk=team.pk)

@login_required(login_url='/account/login/')
def team_kick(request, pk):
    team = get_object_or_404(Team, pk=pk)
    
    if request.method == "POST":
        if 'student_pk' in request.POST:
            student_pk = request.POST["student_pk"]
            student = get_object_or_404(Student, pk=student_pk)
            team.student.remove(student)

        elif 'coach_pk' in request.POST:
            coach_pk = request.POST["coach_pk"]
            coach = get_object_or_404(Coach, pk=coach_pk)
            team.coach.remove(coach)

    return redirect('coaching_app:team_view', pk=team.pk)

def team_settings(request, pk):
    team = get_object_or_404(Team, pk=pk)
    
    # Get the coaches and students
    coaches = team.coach.all()
    students = team.student.all()

    # Get the coaches and students not in this room
    students_not_in_team = Student.objects.filter().exclude(team__pk = pk)
    coaches_not_in_team = Coach.objects.filter().exclude(team__pk = pk)

    if not Coach.objects.get(user = request.user) == None:
        print("this is coach")

    elif not Student.objects.get(user = request.user) == None:
        print("this is student")

    context = {
        'team': team,
        'coaches': coaches,
        'students': students,
        'studentsAdd': students_not_in_team,
        'coachesAdd': coaches_not_in_team
    }
    return render(request, 'coaching_app/team_settings.html', context)

def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)

    if request.method == "POST":
        if request.POST['delete'] == "DELETE":
            team.delete()
            return redirect('coaching_app:index')
    return redirect('coaching_app:team_settings', pk=team.pk)

def team_update(request, pk):
    team = get_object_or_404(Team, pk=pk)
    
    if request.method == "POST":
        updated_name = request.POST['team']
        team.update(name = updated_name)
        return redirect('coaching_app:team_view', pk=team.pk)
    return redirect('coaching_app:team_settings', pk=team.pk)
    

        
                