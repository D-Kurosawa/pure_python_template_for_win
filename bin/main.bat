@echo off
set env_name=python_env_name
set project_name=project_name
set exec_path=%cd%

call conda.bat activate %env_name%

:: Move script path to current
cd /d %~dp0
cd ../

@echo on
python -m %project_name% conf/config.json

call conda.bat deactivate

@echo off
cd /d %exec_path%
