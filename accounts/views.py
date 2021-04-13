from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Accounts

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signupuser.html')
    else:
        print(request.POST['password1'])
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('addToken')
            except IntegrityError:
                return render(request, 'signupuser.html', {'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'signupuser.html', {'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
        if user is None:
            return render(request, 'loginuser.html', {'error':'Username and password did not match'})
        else:
            login(request, user)
            test = (Accounts.objects.filter(user=request.user).values_list('token'))[0]
            print(f"Hello, {test}. .")
            return redirect('home')

@login_required
def logoutuser(request):
    print('test')
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def addToken(request):
    if request.method == 'GET':
        return render(request, 'addToken.html')
    elif request.POST['cciToken'] and Accounts.objects.filter(user=request.user).exists():
        return render(request, 'addToken.html', {'error': 'Token already exist !!!!'})
    elif request.POST['cciToken'] and request.POST['ghToken']:
        token = Accounts()
        token.token = request.POST['cciToken']
        token.gh_token = request.POST['cciToken']
        token.user = request.user
        token.save()
        return redirect('home')
    else:
        return render(request, 'addToken.html', {'error': 'Token are required !!!!'})
