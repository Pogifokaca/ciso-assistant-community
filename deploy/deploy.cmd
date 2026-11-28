@echo off
setlocal
title RegTech deploy
rem ============================================================
rem  RegTech: prenos na kodot od laptopot (C:\ca\reg) na serverot
rem  Dvoklik za start. Prviot pat samo kreira SSH kluc.
rem ============================================================
set "SERVER=ubuntu@13.63.98.108"
set "KEY=%USERPROFILE%\.ssh\regtech_ed25519"
set "REPO=%~dp0.."
set "ARCHIVE=%TEMP%\regtech.tar.gz"
set "SSHOPT=-i "%KEY%" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15"

where ssh >nul 2>nul || (echo [GRESKA] Nema OpenSSH na ovoj kompjuter. & goto :fail)
where tar >nul 2>nul || (echo [GRESKA] Nema tar na ovoj kompjuter. & goto :fail)

if exist "%KEY%" goto :deploy

rem ---------- Prv pat: kreiranje SSH kluc ----------
echo Prv pat: kreiram SSH kluc za vrska so serverot...
if not exist "%USERPROFILE%\.ssh" mkdir "%USERPROFILE%\.ssh"
ssh-keygen -t ed25519 -f "%KEY%" -q -N "" -C "regtech-deploy-%COMPUTERNAME%" || goto :fail
type "%KEY%.pub" | clip
echo.
echo ============================================================
echo  Javniot kluc e KOPIRAN. Zalepete go vo Claude (Ctrl+V).
echo  Ova e javen kluc, bezbedno e da se sprati.
echo ============================================================
type "%KEY%.pub"
echo.
pause
exit /b 0

:deploy
echo [1/3] Pakuvanje na kodot od %REPO% ...
if exist "%ARCHIVE%" del "%ARCHIVE%"
tar -czf "%ARCHIVE%" -C "%REPO%" --exclude=.git --exclude=node_modules --exclude=.venv --exclude=.claude --exclude=__pycache__ --exclude=./db . || goto :fail
for %%A in ("%ARCHIVE%") do echo       Golemina: %%~zA bajti

echo [2/3] Isprakjanje na serverot ...
scp %SSHOPT% "%ARCHIVE%" %SERVER%:/tmp/regtech.tar.gz || goto :fail

echo [3/3] Gradenje na serverot (5-15 minuti, ne zatvorajte go prozorecot) ...
ssh %SSHOPT% %SERVER% "bash ~/regtech-deploy.sh /tmp/regtech.tar.gz" || goto :fail

del "%ARCHIVE%" >nul 2>nul
echo.
echo ============================================================
echo  GOTOVO. Otvorete https://13.63.98.108:8443 i osvezete (Ctrl+F5)
echo ============================================================
pause
exit /b 0

:fail
echo.
echo [GRESKA] Prenosot ne uspea. Napravete slika od ovoj prozorec i pratete ja na Claude.
pause
exit /b 1
