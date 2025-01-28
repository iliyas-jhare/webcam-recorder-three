# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['./src/main.py'],
    pathex=['./src'],
    binaries=[],
    datas=[
        ('src/ui/css/bootstrap.min.css', 'ui/css'),
        ('src/ui/css/bootstrap.min.css.map', 'ui/css'),
        ('src/ui/css/index.css', 'ui/css'),
        ('src/ui/index.html', 'ui')
    ],
    hiddenimports=['config.py', 'logging_wrapper.py', 'recording.py', 'streaming.py'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pip', 'setuptools', 'pyinstaller'],
    noarchive=False,
    optimize=2,   
)

pyz = PYZ(
    a.pure, 
    a.zipped_data
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='webcam_recorder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)
