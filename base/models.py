import ctypes
from ctypes import cdll

lib = ctypes.CDLL('block.so')

def start():
    lib.Start()
    # lib.Set()

def register(name, password):
    register = lib.Register
    register.restype = ctypes.c_char_p
    register.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    result = register(name, password)
    return(result)

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

def getAllTasks():
    gettasks = lib.GetAllTasks
    gettasks.restype = ctypes.c_char_p
    return gettasks()

def getAllUsers():
    getusers = lib.GetAllUsers
    getusers.restype = ctypes.c_char_p
    return getusers()

def postTask(username, title, taskid, tasktype, detail, require, reward, recievetime, deadline, data, keypath, flag):
    posttask = lib.PostTask
    posttask.restype = ctypes.c_char_p
    posttask.argtypes = [ctypes.c_char_p,ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    detail = bytes(str(detail, 'utf-8') + "\tData hash:" + str(upLoad(data, keypath, flag), 'utf-8'), encoding='utf-8')
    result = posttask(username, title, taskid, tasktype, detail, reward, require, recievetime, deadline)
    return result

def postPriTask(title, taskid, tasktype, detail, require, reward, data, keypath, userid):
    posttask = lib.PostPriTask
    posttask.restype = ctypes.c_char_p
    posttask.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,ctypes.c_char_p, ctypes.c_char_p]
    detail = bytes(str(detail, 'utf-8') + "\nData hash:" + str(upLoad(data, keypath), 'utf-8'), encoding='utf-8')
    tasktype = bytes('private', encoding='utf-8')
    result = posttask(title, taskid, tasktype, detail, reward, require,userid)
    return result

def recieveTask(username, taskid):
    recievetask = lib.RecieveTask
    recievetask.restype = ctypes.c_char_p
    recievetask.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    result = recievetask(username, taskid)
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

def getUser(username):
    getuser = lib.GetUser
    getuser.restype = ctypes.c_char_p
    getuser.argtypes = [ctypes.c_char_p]
    result = getuser(username)
    return result

def getProfile(username):
    getprofile = lib.GetProfile
    getprofile.restype = ctypes.c_char_p
    getprofile.argtypes = [ctypes.c_char_p]
    result = getprofile(username)
    return result

def rechargeUser(username, number):
    rechargeuser = lib.Recharge
    rechargeuser.restype = ctypes.c_char_p
    rechargeuser.argtypes = [ctypes.c_char_p,ctypes.c_char_p]
    result = rechargeuser(username, number)
    return result

def addSkills(name, skills):
    addskill = lib.AddSkills
    addskill.restype = ctypes.c_char_p
    addskill.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    result = addskill(name, skills)
    return result

def commitTask(username, taskid, solution, keypath, flag):
    committask = lib.CommitTask
    committask.restype = ctypes.c_char_p
    committask.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    Hash = upLoad(solution, keypath, flag)
    result = committask(username, taskid, Hash)
    return result


def reward(username, taskid, workerid, rate):
    alloreward = lib.AlloReward
    alloreward.restype = ctypes.c_char_p
    alloreward.argtypes = [ctypes.c_char_p,ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    result = alloreward(username, taskid, workerid, rate)
    return result

def upLoad(filepath, keypath, flag):
    upload = cdll.LoadLibrary('ipfs.so').UploadIPFS
    upload.restype = ctypes.c_char_p
    upload.argtype = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    result = upload(filepath, keypath, flag)
    return result

def downLoad(hash, filepath, flag, privatepath):
    download = cdll.LoadLibrary('ipfs.so').CatIPFS
    download.restype = ctypes.c_char_p
    download.argtype = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    result = download(hash, filepath, flag, privatepath)
    return result

def updatetask(taskid, data, publickey, flag):
    update = lib.UpdateTask
    update.restype = ctypes.c_char_p
    update.argtype = [ctypes.c_char_p, ctypes.c_char_p]
    result = update(taskid, upLoad(data, publickey, flag))
    return result