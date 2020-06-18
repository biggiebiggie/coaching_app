from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http import HttpResponseRedirect
from . models import PasswordResetRequest
from django.contrib.auth.decorators import login_required
from coaching_app. models import Coach, Student, Tag
import django_rq
from . messaging import email_message


def login(request):
    context = {}

    if request.method == "POST":
        user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
        if user:
            dj_login(request, user)
            return HttpResponseRedirect(reverse('coaching_app:index'))
        else:
            context = {
                'error': 'Bad username or password.'
            }
    return render(request, 'login_app/login.html', context)


def logout(request):
    dj_logout(request)
    next
    return render(request, 'login_app/login.html')


def request_password_reset(request):
    if request.method == "POST":
        post_user = request.POST['username']
        user = None

        if post_user:
            try:
                user = User.objects.get(username=post_user)
            except:
                print(f"Invalid password request: {post_user}")
        else:
            post_user = request.POST['email']
            try:
                user = User.objects.get(email=post_user)
            except:
                print(f"Invalid password request: {post_user}")
        if user:
            prr = PasswordResetRequest()
            prr.user = user
            prr.save()
            django_rq.enqueue(email_message, {
               'token' : prr.token,
               'email' : prr.user.email,
            })
            return HttpResponseRedirect(reverse('login_app:password_reset'))

    return render(request, 'login_app/request_password_reset.html')

def change_password(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        password = request.POST['password']
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(reverse('login_app:logout'))
    return render(request, 'login_app/change_password.html')


def password_reset(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        token = request.POST['token']

        if password == confirm_password:
            try:
                prr = PasswordResetRequest.objects.get(token=token)
                prr.save()
            except:
                print("Invalid password reset attempt.")
                return render(request, 'login_app/password_reset.html')
                
            user = prr.user
            user.set_password(password)
            user.save()

            return HttpResponseRedirect(reverse('login_app:login'))

    return render(request, 'login_app/password_reset.html')


def sign_up(request):
    context = {}
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_name = request.POST['user']
        email = request.POST['email']
        user_type = request.POST['user_type']
        tag_name = request.POST['tag']
        
        if password == confirm_password:
            if user_type == "coach":
                user = User.objects.create_user(user_name, email, password)
                coach = Coach()
                coach.user = user
                coach.save()
                tag = Tag(tagname = tag_name)
                tag.save()
                coach.tag.add(tag)
                coach.save()
                return HttpResponseRedirect(reverse('login_app:login'))

            elif user_type == "student":
                user = User.objects.create_user(user_name, email, password)
                student = Student()
                student.user = user
                student.save()
                tag = Tag(tagname = tag_name)
                tag.save()
                student.tag.add(tag)
                student.save()
                return HttpResponseRedirect(reverse('login_app:login'))
            else:
                context = {
                    'error': 'Could not create user account - please try again.'
                }
        else:
            context = {
                'error': 'Passwords did not match. Please try again.'
            }
    return render(request, 'login_app/sign_up.html', context)
    

@login_required(login_url='/account/login/')
def delete_account(request):
    if request.method == "POST":
        if request.POST['confirm_deletion'] == "DELETE":            
            user = authenticate(request, username=request.user.username, password=request.POST['password'])
            if user:
                print(f"Deleting user {user}")
                user.delete()
                return HttpResponseRedirect(reverse('login_app:login'))
            else:
                print("fail delete")

    return render(request, 'login_app/delete_account.html')

