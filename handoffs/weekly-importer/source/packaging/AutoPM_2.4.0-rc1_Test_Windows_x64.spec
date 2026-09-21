# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../app.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/个人资料/AI学习圈/SN Auto PM/05-真实项目数据 Real data/Weekly report/AutoPM_Source_20260915/assets', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AutoPM_2.4.0-rc1_Test_Windows_x64',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:/个人资料/AI学习圈/SN Auto PM/05-真实项目数据 Real data/Weekly report/AutoPM_Source_20260915/assets/brand/autopm.ico'],
)
