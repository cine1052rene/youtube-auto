import ctypes, time
from ctypes import wintypes
u = ctypes.windll.user32; res = []
@ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
def cb(h, l):
    if u.IsWindowVisible(h):
        b = ctypes.create_unicode_buffer(512); u.GetWindowTextW(h, b, 512)
        if 'ttapp' in b.value.lower(): res.append(h)
    return True
u.EnumWindows(cb, 0)
for h in res[:1]:
    u.ShowWindow(h, 9); u.keybd_event(0x12,0,0,0); u.keybd_event(0x12,0,2,0); u.SetForegroundWindow(h); u.ShowWindow(h, 3)
print('front', len(res))
