from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from base.models import updatetask,getAllTasks, login, enroll, postTask, postPriTask, getTask, getUser, getProfile, \
    getAllUsers, register, rechargeUser, addSkills, recieveTask, commitTask, getRecord, reward, downLoad
import json
from .form import registerForm, loginForm, taskForm, profileForm, commitForm, rewardForm
import time
from django.contrib import messages
import os

class registerView(View):
    def get(self, request):
        data = {
            "title": "register"
        }
        return render(request, 'register.html', context=data)
    def post(self, request):
        form = registerForm(request.POST or None)
        if form.is_valid():
            name = bytes(form.cleaned_data.get('Name'), encoding='utf-8')
            password = bytes(form.cleaned_data.get('Password'), encoding='utf-8')
            info = bytes(form.cleaned_data.get('Info'), encoding='utf-8')
            result = str(register(name, password),'utf-8')
            if result[0] == '1':
                result = str(enroll(name, password, info), 'utf-8')
                if result[0] =='1':
                    messages.success(request, result[1:])
                    return redirect(reverse('login'))
                else:
                    messages.error(request, result[1:])
                    return redirect(reverse('register'))
            else:
                messages.error(request, result[1:])
                return redirect(reverse('register'))
        else:
            messages.error(request, form.errors)
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
            result = str(login(name), 'utf-8')
            if result[0] == '1':
                request.session['user_id'] = originname
                messages.success(request, result[1:])
                return redirect(reverse('home'))
            else:
                messages.error(request, result[1:])
                return  redirect(reverse('login'))
        else:
            messages.error(request, form.errors)
            return redirect(reverse('login'))

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
        users = json.loads(str(users, 'utf-8'))
        data = {
            "title":"developer",
            "users":users
        }
        return render(request, 'developers.html', context=data)

class profileView(View):
    def get(self, request):
        username = bytes(request.session.get('user_id'), encoding='utf-8')
        user = getProfile(username)
        try:
            user = json.loads(str(user, 'utf-8'))
        except Exception:
            data = {
                "title": "profile",
                "user": str(user, 'utf-8'),
            }
            messages.error(request, 'load error')
        else:
            data = {
                "title": "profile",
                "user": user,
            }
        return render(request, 'profile.html', context=data)
    def post(self, request):
        form = profileForm(request.POST or None)
        if form.is_valid():
            recharge = form.cleaned_data.get('recharge')
            skills= form.cleaned_data.get('skills')
            username = bytes(request.session.get('user_id'), encoding='utf-8')
            if recharge != '':
                result = str(rechargeUser(username, bytes(recharge, encoding='utf-8')), encoding='utf-8')
                if result[0] =='1':
                    pass
                    # messages.success(request, result[1:])
                else:
                    messages.error(request, result[1:])
            if skills != '':
                result = str(addSkills(username, bytes(skills, encoding='utf-8')), encoding='utf-8')
                if result[0] == '1':
                    pass
                    # messages.success(request, result[1:])
                else:
                    messages.error(request, result[1:])
            return redirect('/profile')
        else:
            messages.error(request, form.errors)
            return redirect('/profile')

def getuser(request, userId):
    user = getUser(bytes(userId, encoding='utf-8'))
    user = str(user, 'utf-8')
    # length = len(user)
    # user = user [1:length-1]
    # user = json.loads(user)

    try:
        user = json.loads(user,strict=False)
        print('here')
    except Exception:
        data = {
            "title": "developer",
            "user": user,
        }
    else:
        data = {
            "title": "developer",
            "user": user,
        }
    return render(request, 'developer.html', context=data)

#task

class releaseView(View):
    def get(self, request):
        return render(request, 'release.html')
    def post(self, request):
        # start = time.time()
        form = taskForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            title = bytes(form.cleaned_data.get('title'), encoding='utf-8')
            type = bytes(form.cleaned_data.get('type'),encoding='utf-8')
            detail = bytes(form.cleaned_data.get('detail'), encoding='utf-8')
            reward = bytes(str(form.cleaned_data.get('award')), encoding='utf-8')
            recievetime = form.cleaned_data.get('recievetime').replace('T', ' ')
            recievetime = bytes(recievetime, encoding='utf-8')
            deadline = form.cleaned_data.get('deadline').replace('T', ' ')
            deadline = bytes(deadline, encoding='utf-8')
            requirement = bytes(form.cleaned_data.get('requirment'), encoding='utf-8')
            # data = form.cleaned_data.get('data')
            file = request.FILES['data']
            f = open('file/'+file.name, 'wb')
            for line in file.chunks():
                f.write(line)
            f.close()
            data = bytes('file/'+file.name, encoding='utf-8')
            taskid = bytes(request.session.get('user_id') + form.cleaned_data.get('title'),encoding='utf-8')
            key_name ='PKI/' + form.cleaned_data.get('public_key') + '_PublicKey.pem'
            publickeypath = bytes(key_name, encoding='utf-8')
            flag = bytes(form.cleaned_data.get('flag'), encoding='utf-8')
            username = bytes(request.session.get('user_id'), encoding='utf-8')
            result = postTask(username, title, taskid, type, detail, requirement, reward, recievetime, deadline, data, publickeypath, flag)
            result = str(result, 'utf-8')
            request.session['chId'] = request.session.get('user_id') + form.cleaned_data.get('title')
            os.remove('file/'+file.name)
            # end = time.time()
            # print('任务发布的消耗时间：', end-start)
            if result[0] == '1':
                messages.success(request, result[1:])
                return redirect(reverse('details'))
            else:
                messages.error(request, result[1:])
                return  redirect(reverse('release'))
        else:
            messages.error(request, form.errors)
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
    records = getRecord(bytes(taskId, encoding='utf-8'))
    try:
        task = json.loads(str(task, 'utf-8'))
        records = json.loads(str(records, 'utf-8'))
    except Exception:
        messages.error(request, "获取数据错误")
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

def jointask(request, taskId):
    # start = time.time()
    username = bytes(request.session.get('user_id'), encoding='utf-8')
    result = recieveTask(username, bytes(taskId, encoding='utf-8'))
    result = str(result, 'utf-8')
    if result[0] == '1':
        # end = time.time()
        # print('接受任务的消耗时间为：', end-start)
        messages.success(request, result[1:])
        return redirect('/profile')
    else:
        messages.error(request, result[1:])
        return redirect('/profile')

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
        # start = time.time()
        form = commitForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            # solution = form.cleaned_data.get('solution')
            file = request.FILES['solution']
            f = open('file/' + file.name, 'wb')
            for line in file.chunks():
                f.write(line)
            f.close()
            solution = bytes('file/' + file.name, encoding='utf-8')
            flag = bytes(form.cleaned_data.get('flag'), encoding='utf-8')
            username = bytes(request.session.get('user_id'), encoding='utf-8')
            key_name ='PKI/' + form.cleaned_data.get('public_key') + '_PublicKey.pem'
            publickey = bytes(key_name, encoding='utf-8')
            result = str(commitTask(username, bytes(taskId, encoding='utf-8'), solution, publickey, flag), encoding='utf-8')
            os.remove('file/' + file.name)
            # end = time.time()
            # print('提交解决方案的消耗时间：', end-start)
            print(result)
            if result[0] == '1':
                messages.success(request, result[1:])
                return redirect('/profile')
            else:
                messages.error(request, result[1:])
                return redirect('/profile')
        else:
            messages.error(request, form.errors)
            return redirect('/profile')

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
        if 'reward' in request.POST:
            # start = time.time()
            form = rewardForm(request.POST or None)
            if form.is_valid():
                # workerid = form.cleaned_data.get('workerid')+'\n'
                workerid = form.cleaned_data.get('workerid')

                rate = form.cleaned_data.get('rate')
                workerid = bytes(workerid, encoding='utf-8')
                # print(workerid)
                # workerid = workerid.replace(b'\r\n', b'\n')
                # print(workerid)
                username = bytes(request.session.get('user_id'), encoding='utf-8')
                result = reward(username, bytes(taskId, encoding='utf-8'), workerid,bytes(str(rate), encoding='utf-8'))
                print(result)
                # end = time.time()
                # print('奖励分配的消耗时间：', end-start)
                return redirect('/profile')
            else:
                print('not valid')
                return redirect('/profile')
        else:
            flag = request.POST.get('flag')
            flag = bytes(flag, encoding='utf-8')
            file = request.FILES['data']
            f = open('file/' + file.name, 'wb')
            for line in file.chunks():
                f.write(line)
            f.close()
            data = bytes('file/' + file.name, encoding='utf-8')
            # data = bytes(request.POST.get('data'), encoding='utf-8')
            key_name ='PKI/' + request.POST.get('public_key') + '_PublicKey.pem'
            publickey = bytes(key_name, encoding='utf-8')
            result = str(updatetask(bytes(taskId, encoding='utf-8'), data, publickey, flag))
            os.remove('file/' + file.name)
            if result[0] == '1':
                messages.success(request, result[1:])
                return redirect('/profile')
            else:
                messages.error(request, result[1:])
                return redirect('/profile')

def logout(request):
    request.session.flush()
    return redirect(reverse('home'))

def download(request):
    if request.method == "POST":
        index = bytes(request.POST.get('hash'), encoding='utf-8')
        filepath = bytes(request.POST.get('filepath'), encoding='utf-8')
        flag = request.POST.get('flag')
        flag = bytes(flag, encoding='utf-8')
        privatepath = 'PKI/'+request.POST.get('private_key')+ '_PrivateKey.pem'
        privatepath = bytes(privatepath, encoding='utf-8')
        text = str(downLoad(index, filepath, flag, privatepath), encoding='utf-8')
        return render(request, 'download.html', {'context': text})
    return render(request, 'download.html', {'context': ""})

class privateView(View):
    def get(self, request):
        return render(request, 'private.html')
    def post(self, request):
        form = taskForm(request.POST or None)
        if form.is_valid():
            title = bytes(form.cleaned_data.get('title'), encoding='utf-8')
            detail = bytes(form.cleaned_data.get('detail'), encoding='utf-8')
            reward = bytes(str(form.cleaned_data.get('award')), encoding='utf-8')
            requirement = bytes(form.cleaned_data.get('requirment'), encoding='utf-8')
            data = bytes(form.cleaned_data.get('data'), encoding='utf-8')
            userid = request.session.get('user_id')
            taskid = bytes(userid+ form.cleaned_data.get('title'), encoding='utf-8')
            publickeypath = bytes(form.cleaned_data.get('public_key'), encoding='utf-8')
            userid = bytes(userid, encoding='utf-8')
            result = postPriTask(title, taskid, detail, requirement, reward, data, publickeypath, userid)
            request.session['chId'] =userid+ form.cleaned_data.get('title')
            print(result)
            return redirect(reverse('details'))
        else:
            print(form.errors)
            return redirect(reverse('private'))
