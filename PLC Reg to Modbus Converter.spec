# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['flask', 'socketio.namespace', 'engineio.async_drivers.threading', 'flask_cors', 'PIL.Image', 'pystray', 'bidict', 'flask_session', 'cachelib', 'wmi', 'pywintypes']
hiddenimports += collect_submodules('engineio')
hiddenimports += collect_submodules('werkzeug')


a = Analysis(
    ['D:\\Personal Projects\\MB Converter\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\Personal Projects\\MB Converter/Convert.py', '.'), ('D:\\Personal Projects\\MB Converter/Blueprints', 'Blueprints'), ('D:\\Personal Projects\\MB Converter/templates', 'templates'), ('D:\\Personal Projects\\MB Converter/static', 'static'), ('D:\\Personal Projects\\MB Converter/logo', 'logo')],
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
    name='PLC Reg to Modbus Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Personal Projects\\MB Converter\\logo\\plc_to_modbus.ico'],
    manifest='elevated.manifest',
)
