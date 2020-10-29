@echo off
set /p env_name="Input virtual enviroment name : "
echo on

call conda.bat activate %env_name%

@echo off
if %errorlevel% neq 0 (
  echo;
  echo Error : Can not activate [%env_name%]
  exit /b
)
echo on

call conda list -e            > ../../requirements/requirements_conda.txt
call pip list --format freeze > ../../requirements/requirements_pip.txt
call conda.bat deactivate
