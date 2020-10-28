@echo off
:: 仮想環境名の入力要求
set /p env_name="Input virtual enviroment name : "

:: 日付をyyyymmdd形式で取得
set date_str=%date:~-10,4%%date:~-5,2%%date:~-2,2%
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

call conda list -e > requirements_conda_%env_name%_%date_str%.txt
call pip list --format freeze > requirements_pip_%env_name%_%date_str%.txt
call conda.bat deactivate
