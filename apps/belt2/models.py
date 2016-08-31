from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}')

class UserManager(models.Manager):
    def register(self, birthday, name, email, create_password, conf_password):
        errors = []
        if len(email) < 6:
            errors.append("Email address is too short!")
        if not EMAIL_REGEX.match(email):
            errors.append("Email address is invalid")
        if Users.objects.filter(email=email).exists() == True:
            errors.append("Email already exsists! Please log in.")
        if len(email) > 30:
            errors.append("Email address is too Long!")
        if birthday == "":
            errors.append("Please enter your birthday.")
        if name == "":
            errors.append("Name cannot be empty!")
        if create_password != conf_password:
            errors.append("Passwords don't match! Please try again.")
        if len(create_password) < 8:
            errors.append("Password is too short!")
        if not PASSWORD_REGEX.match(create_password):
            errors.append("Password is invalid, please try again.")
        if len(create_password) > 40:
            errors.append("Password is too Long!")
        if errors == []:
            hashed_pass = bcrypt.hashpw(create_password.encode(), bcrypt.gensalt())
            user = Users.objects.create(email = email, password = hashed_pass, name=name, birthday=birthday)
            return (True, errors, user)
        else:
            return(False, errors)


    def userlogin(self, logemail, login_password):
        from bcrypt import hashpw, gensalt
        login_errors = []
        if Users.objects.filter(email=logemail).exists() == False:
            login_errors.append("Sorry, no user found. Please try again.")
            return (False, login_errors)
        else:
            user = Users.objects.get(email=logemail)
            password = user.password.encode()
            loginpass = login_password.encode()
            if hashpw(loginpass, password) == password:
                return (True, login_errors, user)
            else:
                login_errors.append("Sorry, no password match")
                return (False, login_errors)

    def taskcheck(self, task, date, time, user):
        errors = []
        if task == "":
            errors.append("Task cannot be blank!")
        if time == "":
            errors.append("Time cannot be empty!")
        if date == "":
            errors.append("Date cannot be empty!")
        if date < str(datetime.today() - timedelta(1)):
            errors.append("DateMust be a future datetime")
        if errors == []:
            task = Tasks.objects.create(task = task, status = "pending", date=date, time=time, user=user)
            return (True, errors, task)
        else:
            return(False, errors)

    def taskupdate(self, task, date, time, user, status,id):
        errors = []
        if task == "":
            errors.append("Task cannot be blank!")
        if time == "":
            errors.append("Time cannot be empty!")
        if date == "":
            errors.append("Date cannot be empty!")
        if date < str(datetime.today() - timedelta(1)):
            errors.append("Date Must be a future datetime")
        if errors == []:
            task = Tasks.objects.filter(id=id).update(task = task, status = status, date=date, time=time, user=user)
            return (True, errors, task)
        else:
            return(False, errors)

class Users(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=130)
    password = models.CharField(max_length=200)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    usermanager = UserManager()
    objects = models.Manager()

class Tasks(models.Model):
    task = models.CharField(max_length=1000)
    status = models.CharField(max_length=10)
    time = models.TimeField()
    date = models.DateField()
    user = models.ForeignKey(Users)

    taskmanager = UserManager()
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
