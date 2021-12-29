import ctypes

def screener():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    SCREEN_SIZE = screensize
    DISPLAY_SIZE = SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2
    A_scroll, B_scroll = DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2
    return SCREEN_SIZE, DISPLAY_SIZE, A_scroll, B_scroll