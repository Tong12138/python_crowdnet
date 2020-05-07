import ctypes


print('收到回复可收到回复')
lib = ctypes.CDLL('block.so')

lib.Start()

lib.Set()