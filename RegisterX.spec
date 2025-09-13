# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['flask', 'socketio.namespace', 'engineio.async_drivers.threading', 'flask_cors', 'PIL.Image', 'pystray', 'bidict', 'flask_session', 'cachelib', 'wmi', 'pywintypes']
hiddenimports += collect_submodules('engineio')
hiddenimports += collect_submodules('werkzeug')


a = Analysis(
    ['D:\\Personal Projects\\RegisterX\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\Personal Projects\\RegisterX/Convert.py', '.'), ('D:\\Personal Projects\\RegisterX/Blueprints', 'Blueprints'), ('D:\\Personal Projects\\RegisterX/templates', 'templates'), ('D:\\Personal Projects\\RegisterX/static', 'static'), ('D:\\Personal Projects\\RegisterX/logo', 'logo')],
    hiddenimports=hiddenimports,
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
    name='RegisterX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Personal Projects\\RegisterX\\logo\\plc_to_modbus.ico'],
    manifest='elevated.manifest',
)
