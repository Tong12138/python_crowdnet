from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from base.models import getAllTasks, login, postTask, getTask, getUser, getAllUsers
import json
from .form import registerForm, loginForm, challengeForm
class homeView(View):
    def get(self, request):
        tasks = getAllTasks()
        tasks = str(tasks, 'utf-8')
        tasks = json.loads(tasks)
        data = {
            "title": "BUAA",
            "challenge": tasks,
        }
        return render(request, 'home.html', context=data)


class developerView(View):
    def get(self, request):
        users = getAllUsers()
        print(users)
        users = json.loads(str(users, 'utf-8'))
        data = {
            "title":"developer",
            "users":users
        }
        return render(request, 'developers.html', context=data)

# def developer(request):
#     return render(request, 'developers.html')

class registerView(View):
    def get(self, request):
        data = {
            "title": "register"
        }
        return render(request, 'register.html', context=data)
    def post(self, request):
        form = registerForm(request.POST or None)
        # form.register_time = datetime.datetime.now().strftime('%Y-%m-%d')
        if form.is_valid():
            name = form.cleaned_data.get('Name')
            # print(name)
            name = bytes(name, encoding='utf-8')
            info = form.cleaned_data.get('Info')
            info = bytes(info, encoding='utf-8')
            result = registerUser(name, info)
            print(result)
            return redirect(reverse('home'))
        else:
            errors = form.errors
            print(errors)
            return redirect(reverse('register'))

class loginView(View):
    def get(self, request):
        data = {
            "title": "login"
        }
        return render(request, 'login.html',context=data)
    def post(self, request):
        form = loginForm(request.POST or None)
        if form.is_valid():
            originname = form.cleaned_data.get('Name')
            name = bytes(originname, encoding='utf-8')
            info = form.cleaned_data.get('Info')
            info = bytes(info, encoding='utf-8')
            result = login(name, info)
            result = str(result, 'utf-8')
            if result[0] == '1':
                request.session['user_id'] = originname
                return redirect(reverse('home'))
            else:
                print('用户名或密码错误')
                return  redirect(reverse('login'))
        else:
            print(form.errors.get_json_data())
            return redirect(reverse('login'))


class releaseView(View):
    def get(self, request):
        return render(request, 'release.html')
    def post(self, request):
        form = challengeForm(request.POST or None)
        if form.is_valid():
            title = bytes(form.cleaned_data.get('title'), encoding='utf-8')
            detail = bytes(form.cleaned_data.get('detail'), encoding='utf-8')
            reward = bytes(str(form.cleaned_data.get('award')), encoding='utf-8')
            requirement = bytes(form.cleaned_data.get('requirment'), encoding='utf-8')
            id = request.session.get('user_id') + form.cleaned_data.get('title')
            taskid = bytes(id, encoding='utf-8')
            result = postTask(title, taskid, detail, requirement, reward)
            request.session['chId'] = id
            print(result)
            return redirect(reverse('details'))
        else:
            print(form.errors.get_json_data())
            return redirect(reverse('release'))

def details(request):
    ch_id = request.session.get('chId')
    task = getTask(bytes(ch_id, encoding='utf-8'))
    try:
        task = json.loads(str(task, 'utf-8'))
    except Exception:
        data = {
            "title": "Details",
            "task": str(task, 'utf-8'),
        }
    else:
        data = {
            "title": "Details",
            "task": task,
        }
    return render(request, 'details.html', context=data)


def task(request, taskId):
    task = getTask(bytes(taskId, encoding='utf-8'))
    try:
        task = json.loads(str(task, 'utf-8'))
    except Exception:
        data = {
            "title": "Details",
            "task": str(task, 'utf-8'),
        }
    else:
        data = {
            "title": "Details",
            "task": task,
        }
    # data = {
    #     "title": "TaskDetails",
    #     "task": task,
    #     # "hoster": task.hoster
    # }
    return render(request, 'task.html', context=data)

def profile(request, userId):
    user = getUser(bytes(userId, encoding='utf-8'))
    # hist_chal = user.challenge_set.all()
    try:
        user = json.loads(str(user, 'utf-8'))
    except Exception:

        data = {
            "title": "profile",
            "user": str(user,'utf-8'),
            # "history": hist_chal
        }
    else:
        data = {
            "title": "profile",
            "user": user,
            # "history": hist_chal
        }
    return render(request, 'profile.html', context=data)

def logout(request):
    request.session.flush()
    return redirect(reverse('home'))