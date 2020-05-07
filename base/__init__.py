import ctypes

lib = ctypes.CDLL('block.so')

lib.Start()

# lib.Set()