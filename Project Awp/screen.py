import ctypes
import numpy as np

capture_screen = ctypes.CDLL('./capture_awp.dll')

class CapturedImage(ctypes.Structure):
    _fields_ = [("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("data", ctypes.POINTER(ctypes.c_ubyte))]

def screenshot():
    captured_image = capture_screen.captureScreen(1280, 720)
    data_array = np.ctypeslib.as_array(captured_image.data, shape=(captured_image.height, captured_image.width, 3))
    capture_screen.freeCapturedImage.argtypes = [ctypes.POINTER(CapturedImage)]
    capture_screen.freeCapturedImage(ctypes.byref(captured_image))
    return data_array

def run():
    capture_screen.captureScreen.restype = CapturedImage