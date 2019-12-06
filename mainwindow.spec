# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['mainwindow.py'],
             pathex=['/home/alexanderb/Downloads/cpsc-362-python-qt-search'],
             binaries=[],
             datas=[('assets/tika/tika-server.jar', 'data_files'), ('assets/tika/tika-server.jar.md5', 'data_files'), ('assets/tika/tika.log', 'data_files'), ('assets/tika/tika-server.log', 'data_files')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='mainwindow',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
