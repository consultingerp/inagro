del *.pyc /q
del *.pyo /q
del *.bak /q
del Thumbs.db /q

@echo off
rem --------------------------------------------------
rem clean
rem Will delete all __pycache___ directories in 
rem this directory recursively.
rem
rem G.Berthiaume 2019
rem --------------------------------------------------
rem
set /a count = 1
for /d /r . %%d in (__pycache__) do @if exist "%%d"  set /a count += 1 && rd /s/q "%%d"

echo Successfully deleted %count% files.