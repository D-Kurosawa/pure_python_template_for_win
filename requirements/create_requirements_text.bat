@echo off
:: 仮想環境名の入力要求
set /p env_name="Input virtual enviroment name : "
echo on

call conda.bat activate %env_name%

@echo off
:: activate失敗時に"errorlevel"に1が入ることを利用してエラーチェック
if %errorlevel% neq 0 (
  echo;
  echo Error : Can not activate [%env_name%]
  exit /b
)
echo on

call conda list -e > requirements_conda.txt
call pip list --format freeze > requirements_pip.txt
call conda.bat deactivate
