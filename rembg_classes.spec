# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['rembg_classes.py'],
    pathex=[],
    binaries=[('C:\\Users\\Jonas\\Documents\\Python Scripts\\remove_bg\\env_r\\Lib\\site-packages\\scipy.libs\\*.dll', '.')],
    datas=[],
    hiddenimports=['scipy.sparse.linalg._isolve._iterative', 'scipy.sparse.linalg._isolve'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='rembg_classes',
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
)
