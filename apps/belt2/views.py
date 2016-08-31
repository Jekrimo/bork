from django.shortcuts import render, redirect
from . import models
from models import Users, Tasks
from datetime import datetime

def index(request):
    return render(request, "belt2/index.html")

def createuser(request):
    if request.method == 'POST':
        user = Users.usermanager.register(email=request.POST['email'],birthday= request.POST['birthday'], name=request.POST['name'],conf_password = request.POST['passconf'], create_password=request.POST['password'])
        if user[0] == True:
            print user[2]
            request.session['user'] = user[2].id
            return redirect('/show')
        else:
            context = {
                'errors' : user[1]
            }
            return render(request, "belt2/index.html", context)

def login(request):
    if request.method == 'POST':
        user = Users.usermanager.userlogin(logemail=request.POST['logemail'],login_password=request.POST['logpass'])
        if user[0] == True:
            request.session['user'] = user[2].id
            print user[2].name
            return redirect('/show')
        else:
            context = {
                'logerrors' : user[1]
            }
            return render(request, "belt2/index.html", context)
    else:
        return redirect('/')
    return redirect("/")

def show(request):
    name= request.session['user']
    print "(((())))"
    user= Users.objects.get(id=name)
    today= datetime.today()
    todaytasks = Tasks.objects.filter(date=today, user=user)
    futuretask = Tasks.objects.all().exclude(date=today).filter(user=user)
    context={
        'user' : user,
        'todaytask' : todaytasks,
        'futuretask' : futuretask,
        'today' : datetime.now()
    }
    return render(request, "belt2/show.html", context)

def create(request):
    userid = request.session['user']
    user= Users.objects.get(id=userid)
    if request.method == 'POST':
        task = Tasks.taskmanager.taskcheck(time=request.POST['time'],date=request.POST['taskdate'], task=request.POST['task'], user=user)
        if task[0] == True:
            return redirect('/show')
        else:
            errors = task[1]
            context={
                'taskerror' : errors,
                'user' : user
            }
            return render(request, "belt2/show.html", context)

def edit(request, id):
    thistask = Tasks.objects.get(id=id)
    context={
        'task' : thistask,
    }
    return render(request, "belt2/edit.html", context)

def update(request, id):
    thistask = Tasks.objects.get(id=id)
    userid = request.session['user']
    user= Users.objects.get(id=userid)
    if request.method == 'POST':
        task = Tasks.taskmanager.taskupdate(id=id,time=request.POST['time'],date=request.POST['taskdate'], task=request.POST['task'], user=user, status=request.POST['status'])
        if task[0] == True:
            return redirect('/show')
        else:
            print task[1]
            context={
                'taskerror' : task[1],
                'task' : thistask
            }
            return render(request, "belt2/edit.html", context)
def delete(request, id):
    Tasks.objects.filter(id=id).delete()
    return redirect('/show')

def logout(request):
    request.session.clear()
    return redirect('/')
