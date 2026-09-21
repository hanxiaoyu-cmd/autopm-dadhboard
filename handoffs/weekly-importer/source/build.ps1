$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$buildPython = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $buildPython)) { throw 'Run start.ps1 once to prepare Python.' }
& $buildPython -m pip install pyinstaller
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller installation failed.' }
$env:PYTHONPATH = Join-Path $PSScriptRoot 'tests'
& $buildPython -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Tests failed.' }
& $buildPython -m autopm.brand
if ($LASTEXITCODE -ne 0) { throw 'Brand asset generation failed.' }
$packageVersion = & $buildPython -c 'from autopm import __version__; print(__version__)'
if ($LASTEXITCODE -ne 0) { throw 'Unable to read package version.' }
& $buildPython -m PyInstaller --noconfirm --clean --onefile --windowed --noupx --icon "$PSScriptRoot/assets/brand/autopm.ico" --add-data "$PSScriptRoot/assets;assets" --specpath packaging --name "AutoPM_${packageVersion}_Test_Windows_x64" app.py
if ($LASTEXITCODE -ne 0) { throw 'Build failed.' }
