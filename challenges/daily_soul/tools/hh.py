# 파이썬 ctypes로 Higgsfield 앱 창 앞으로 + 클릭 + 캡처 (Add-Type 안 씀)
import ctypes, time, sys
from ctypes import wintypes
from PIL import ImageGrab
u = ctypes.windll.user32
u.SetProcessDPIAware()
def find(kw='Higgsfield', no='Discord'):
    res = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    def cb(h, l):
        if u.IsWindowVisible(h):
            b = ctypes.create_unicode_buffer(512); u.GetWindowTextW(h, b, 512)
            t = b.value
            if kw in t and no not in t and 'ttapp' not in t: res.append(h)
        return True
    u.EnumWindows(cb, 0); return res[0] if res else None
def front():
    h = find(); u.ShowWindow(h, 9); u.keybd_event(0x12,0,0,0); u.keybd_event(0x12,0,2,0)
    u.SetForegroundWindow(h); time.sleep(0.4); u.ShowWindow(h, 3); time.sleep(0.6)
def clk(x, y):
    u.SetCursorPos(x, y); time.sleep(0.2); u.mouse_event(2,0,0,0,0); time.sleep(0.06); u.mouse_event(4,0,0,0,0)
def cap(p): ImageGrab.grab().save(p)
if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'click':  # click x y out
        front(); clk(int(sys.argv[2]), int(sys.argv[3])); time.sleep(float(sys.argv[5]) if len(sys.argv)>5 else 3); cap(sys.argv[4])
    elif cmd == 'cap':
        front(); cap(sys.argv[2])
    elif cmd == 'heart':  # tile x y name : open → heart → close
        O='C:/project/youtube/challenges/daily_soul/tmp/'; n=sys.argv[4]
        front(); clk(int(sys.argv[2]), int(sys.argv[3])); time.sleep(5); cap(O+n+'.png')
        clk(1747, 983); time.sleep(3); cap(O+'hk_'+n+'.png')
        clk(1879, 70); time.sleep(3)
