call conda list -e > requirements_conda.txt
call pip freeze > requirements_pip.txt

@echo off
del /f "%~dp0%~nx0"
