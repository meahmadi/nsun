c:\Python27\Scripts\pyinstaller.exe  server.py --icon=icon.ico 
xcopy templates  dist\server\templates /f /e /y
xcopy static  dist\server\static /f /e /y
rem xcopy ir  dist\server\ir /f /e /y
xcopy server.pyc dist\server
cd dist\server
del /S *.py

cd ..\..
c:\Python27\Scripts\pyinstaller.exe  agent.py --icon=icon.ico

pause

