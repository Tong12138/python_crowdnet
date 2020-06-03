from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from base.models import getAllTasks, login, enroll, postTask, getTask, getUser, getAllUsers, register, rechargeUser, addSkills, recieveTask, commitTask, getRecord, reward, downLoad
import json
from .form import registerForm, loginForm, challengeForm, profileForm, commitForm, rewardForm
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
            name = bytes(form.cleaned_data.get('Name'), encoding='utf-8')
            password = bytes(form.cleaned_data.get('Password'), encoding='utf-8')
            info = form.cleaned_data.get('Info')
            info = bytes(info, encoding='utf-8')
            result = register(name, password)
            print(result)
            result = enroll(name, password, info)
            print(result)
            return redirect(reverse('login'))
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
            # password = form.cleaned_data.get('Password')
            # password = bytes(password, encoding='utf-8')
            # info = form.cleaned_data.get('Info')
            # info = bytes(info, encoding='utf-8')
            result = login(name)
            result = str(result, 'utf-8')
            print(result)
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
            data = bytes(form.cleaned_data.get('data'), encoding='utf-8')
            id = request.session.get('user_id') + form.cleaned_data.get('title')
            taskid = bytes(id, encoding='utf-8')
            publickeypath = bytes(form.cleaned_data.get('public_key'), encoding='utf-8')
            result = postTask(title, taskid, detail, requirement, reward, data, publickeypath)
            request.session['chId'] = id
            print(result)
            return redirect(reverse('details'))
        else:
            print(form.errors.get_json_data())
            return redirect(reverse('release'))

class profileView(View):
    def get(self, request, userId):
        user = getUser(bytes(userId, encoding='utf-8'))
        try:
            user = json.loads(str(user, 'utf-8'))
        except Exception:
            data = {
                "title": "profile",
                "user": str(user, 'utf-8'),
            }
        else:
            data = {
                "title": "profile",
                "user": user,
            }
        return render(request, 'profile.html', context=data)
    def post(self, request, userId):
        form = profileForm(request.POST or None)
        if form.is_valid():
            recharge = form.cleaned_data.get('recharge')
            skills= form.cleaned_data.get('skills')
            if recharge != '':
                result = rechargeUser(bytes(recharge, encoding='utf-8'))
                print(result)
            if skills != '':
                result = addSkills(bytes(skills, encoding='utf-8'))
                print(result)
            return redirect('/profile/'+ userId)
        else:
            return redirect('/profile/'+ userId)

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
    records = getRecord(bytes(taskId, encoding='utf-8'))
    try:
        task = json.loads(str(task, 'utf-8'))
        records = json.loads(str(records, 'utf-8'))
    except Exception:
        data = {
            "title": "Details",
            "task": str(task, 'utf-8'),
            "records": str(records, 'utf-8'),
        }
    else:
        data = {
            "title": "Details",
            "task": task,
            "records": records,
        }
    return render(request, 'task.html', context=data)

def jointask(request,taskId):
    result = recieveTask(bytes(taskId, encoding='utf-8'))
    result = str(result, 'utf-8')
    if result[0] == '1':
        return redirect('/profile/'+ request.session.get('user_id'))
    else:
        print(result)
        return redirect('/profile/'+ request.session.get('user_id'))

class mytaskView(View):
    def get(self, request, taskId):
        task = getTask(bytes(taskId, encoding='utf-8'))
        try:
            task = json.loads(str(task, 'utf-8'))
        except Exception:
            data = {
                "title": "Mytask",
                "task": str(task, 'utf-8'),
            }
        else:
            data = {
                "title": "Mytask",
                "task": task,
            }
        return render(request, 'mytask.html', context=data)

    def post(self, request, taskId):

        form = commitForm(request.POST or None)
        if form.is_valid():
            solution = form.cleaned_data.get('solution')
            publickey = bytes(form.cleaned_data.get('public_key'), encoding='utf-8')
            result = commitTask(bytes(taskId, encoding='utf-8'),bytes(solution, encoding='utf-8'), publickey)
            print(result)
            return redirect('/profile/' + request.session.get('user_id'))
        else:
            print('not valid')
            return redirect('/profile/' + request.session.get('user_id'))

class rewardView(View):
    def get(self, request, taskId):
        task = getTask(bytes(taskId, encoding='utf-8'))
        try:
            task = json.loads(str(task, 'utf-8'))
        except Exception:
            data = {
                "title": "Reward",
                "task": str(task, 'utf-8'),
            }
        else:
            data = {
                "title": "Reward",
                "task": task,
            }
        return render(request, 'reward.html', context=data)

    def post(self, request, taskId):
        form = rewardForm(request.POST or None)
        if form.is_valid():
            workerid = form.cleaned_data.get('workerid')+'\n'
            rate = form.cleaned_data.get('rate')
            workerid = bytes(workerid, encoding='utf-8')
            print(workerid)
            workerid = workerid.replace(b'\r\n', b'\n')
            print(workerid)
            result = reward(bytes(taskId, encoding='utf-8'), workerid,bytes(str(rate), encoding='utf-8'))
            print(result)
            return redirect('/profile/' + request.session.get('user_id'))
        else:
            print('not valid')
            return redirect('/profile/' + request.session.get('user_id'))


def profile(request, userId):
    user = getUser(bytes(userId, encoding='utf-8'))
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

def download(request):
    if request.method == "POST":
        index = bytes(request.POST.get('hash'), encoding='utf-8')
        filepath = bytes(request.POST.get('filepath'), encoding='utf-8')
        text = str(downLoad(index, filepath), 'utf-8')
        return render(request, 'download.html', {'context': text})
    return render(request, 'download.html', {'context': ""})