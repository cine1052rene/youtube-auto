# 디스코드 창 조작 + OCR + 클립보드 (당선작 링크 수집용)
import ctypes, time, subprocess, sys, os
from ctypes import wintypes
from PIL import ImageGrab
u = ctypes.windll.user32; u.SetProcessDPIAware()
OCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ocr.ps1')
def find():
    res = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
    def cb(h, l):
        if u.IsWindowVisible(h):
            b = ctypes.create_unicode_buffer(512); u.GetWindowTextW(h, b, 512)
            if b.value.endswith('- Discord'): res.append(h)
        return True
    u.EnumWindows(cb, 0); return res[0] if res else None
def front():
    subprocess.run(['powershell','-NoProfile','-File',os.path.join(os.path.dirname(OCR),'win.ps1'),'-title','Discord','-max'],capture_output=True)
    subprocess.run(['powershell','-NoProfile','-File',os.path.join(os.path.dirname(OCR),'dc.ps1'),'-out',r'C:	mp_f.png','-wait','300'],capture_output=True); return
    h = find(); u.ShowWindow(h, 9); u.keybd_event(0x12,0,0,0); u.keybd_event(0x12,0,2,0); u.SetForegroundWindow(h); time.sleep(0.3); u.ShowWindow(h, 3); time.sleep(0.3)
def clk(x, y, right=False):
    u.SetCursorPos(int(x), int(y)); time.sleep(0.15)
    a, b = (8, 16) if right else (2, 4)
    u.mouse_event(a,0,0,0,0); time.sleep(0.05); u.mouse_event(b,0,0,0,0)
def scroll(x, y, amt):
    u.SetCursorPos(int(x), int(y)); time.sleep(0.1); u.mouse_event(0x0800, 0, 0, int(amt), 0)
def cap(p='C:/tmp/_d.png'):
    ImageGrab.grab().save(p); return p
def ocr(p):
    out = subprocess.run(['powershell', '-NoProfile', '-File', OCR, '-img', os.path.normpath(p)], capture_output=True).stdout.decode('utf-8', 'ignore')
    lines, words = [], []
    for l in out.splitlines():
        f = l.split('\t')
        if f[0] == 'W' and len(f) >= 6: words.append((int(f[1]), int(f[2]), int(f[3]), int(f[4]), f[5]))
        elif len(f) >= 5 and f[0].isdigit(): lines.append((int(f[0]), int(f[1]), int(f[2]), int(f[3]), f[4]))
    return lines, words
def clip():
    return subprocess.run(['powershell', '-NoProfile', '-Command', 'Get-Clipboard'], capture_output=True).stdout.decode('utf-8', 'ignore').strip()
