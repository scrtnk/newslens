# news_briefing.spec
# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 6.x syntax — block_cipher and a.zipped_data were removed in v6

a = Analysis(
    ['app/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('assets/icon.png', 'assets'), ('.env', '.')],
    hiddenimports=['feedparser', 'openai', 'pydantic', 'pydantic_settings'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name='NewsLens',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    # icon= is ignored on macOS for EXE; set on BUNDLE below
)

coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas,
    strip=False, upx=True, upx_exclude=[], name='NewsLens',
)

app = BUNDLE(
    coll,
    name='NewsLens.app',
    # For a polished icon, convert assets/icon.png to assets/icon.icns first:
    #   sips -s format icns assets/icon.png --out assets/icon.icns
    # icon='assets/icon.icns',
    bundle_identifier='com.scrtnk.newslens',
    info_plist={
        'LSUIElement': True,          # hides from Dock — pure menu bar app
        'NSHighResolutionCapable': True,
    },
)
