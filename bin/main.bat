@echo off
set dir_name=project_name
set execpath=%cd%

:: 強制的にスクリプトが置かれているパスをカレントにする
cd /d %~dp0
cd ../

@echo on
python -m %project_dir% conf/config.json

@echo off
cd /d %execpath%
