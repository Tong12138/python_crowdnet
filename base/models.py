import ctypes

lib = ctypes.CDLL('block.so')

def start():
    lib.Start()
    # lib.Set()

def getAllTasks():
    gettasks = lib.GetAllTasks
    gettasks.restype = ctypes.c_char_p
    return gettasks()

def getAllUsers():
    getusers = lib.GetAllUsers
    getusers.restype = ctypes.c_char_p
    return getusers()

def register(name, password):
    register = lib.Register
    register.restype = ctypes.c_char_p
    register.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    result = register(name, password)
    print(result)


def enroll(name, password, info):
    enrolluser = lib.Enroll
    enrolluser.restype = ctypes.c_char_p
    enrolluser.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    result= enrolluser(name, password, info)
    return result

def login(name):
    loginuser = lib.Login
    loginuser.restype = ctypes.c_char_p
    loginuser.argtypes = [ctypes.c_char_p]
    result = loginuser(name)
    return result


def postTask(title, taskid, detail, require, reward):
    posttask = lib.PostTask
    posttask.restype = ctypes.c_char_p
    posttask.argtypes = [ctypes.c_char_p, ctypes.c_char_p,ctypes.c_char_p, ctypes.c_char_p,ctypes.c_char_p, ctypes.c_char_p]

    tasktype = bytes('one2one', encoding='utf-8')
    # detail =b ytes('detaildetaildetail', encoding='utf-8')
    result = posttask(title, taskid, tasktype, detail, reward, require)
    return result

def recieveTask(taskid):
    recievetask = lib.RecieveTask
    recievetask.restype = ctypes.c_char_p
    recievetask.argtypes = [ctypes.c_char_p]
    result = recievetask(taskid)
    return result

def getTask(taskid):
    gettask = lib.GetTask
    gettask.restype = ctypes.c_char_p
    gettask.argtypes = [ctypes.c_char_p]
    result = gettask(taskid)
    return result

def getRecord(taskid):
    getrecord = lib.GetRecord
    getrecord.restype = ctypes.c_char_p
    getrecord.argtypes = [ctypes.c_char_p]
    result = getrecord(taskid)
    return result

def getUser(userid):
    getuser = lib.GetUser
    getuser.restype = ctypes.c_char_p
    # getuser.argtypes = [ctypes.c_char_p]
    result = getuser()
    return result

def rechargeUser(number):
    rechargeuser = lib.Recharge
    rechargeuser.restype = ctypes.c_char_p
    rechargeuser.argtypes = [ctypes.c_char_p]
    result = rechargeuser(number)
    return result

def addSkills(skills):
    addskill = lib.AddSkills
    addskill.restype = ctypes.c_char_p
    addskill.argtypes = [ctypes.c_char_p]
    result = addskill(skills)
    return result

def commitTask(taskid, solution):
    committask = lib.CommitTask
    committask.restype = ctypes.c_char_p
    committask.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    result = committask(taskid, solution)
    return result


def reward(taskid, workerid, rate):
    alloreward = lib.AlloReward
    alloreward.restype = ctypes.c_char_p
    alloreward.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    result = alloreward(taskid, workerid, rate)
    return result