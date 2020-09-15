@echo off
pushd %~dp0
set PYTHONPATH=%CD%
popd
python -m eggscript_src %*