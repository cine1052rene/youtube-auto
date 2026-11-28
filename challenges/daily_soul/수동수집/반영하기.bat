@echo off
chcp 65001 >nul
cd /d "%~dp0.."
set PY=C:\Users\cine1\AppData\Local\Programs\Python\Python312\python.exe
set PYTHONIOENCODING=utf-8
echo [1/3] 수동수집 폴더 읽기
"%PY%" tools\manual_import.py
echo.
echo [2/3] 공유 링크에서 프롬프트 받기 (몇 분 걸릴 수 있음)
"%PY%" tools\share_fetch.py
echo.
echo [3/3] 기록 페이지 다시 만들기
"%PY%" tools\build_archive.py
start "" "data\archive\index.html"
echo 완료. 창을 닫아도 됩니다.
pause
