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

def login(name, info):
    registeruser = lib.Register
    registeruser.restype = ctypes.c_char_p
    registeruser.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    result= registeruser(name, info)
    # print('result', result)
    return result

def postTask(title, taskid, detail, require, reward):
    posttask = lib.PostTask
    posttask.restype = ctypes.c_char_p
    posttask.argtypes = [ctypes.c_char_p, ctypes.c_char_p,ctypes.c_char_p, ctypes.c_char_p,ctypes.c_char_p, ctypes.c_char_p]

    tasktype = bytes('one2one', encoding='utf-8')
    # detail =b ytes('detaildetaildetail', encoding='utf-8')
    print(require)
    result = posttask(title, taskid, tasktype, detail, reward, require)

    return result

def getTask(taskid):
    gettask = lib.GetTask
    gettask.restype = ctypes.c_char_p
    gettask.argtypes = [ctypes.c_char_p]
    result = gettask(taskid)
    return result


def getUser(userid):
    getuser = lib.GetUser
    getuser.restype = ctypes.c_char_p
    # getuser.argtypes = [ctypes.c_char_p]
    result = getuser()
    return result