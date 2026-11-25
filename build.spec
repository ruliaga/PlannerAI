# build.spec
a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.yaml', '.'),
        ('ui/style.qss', 'ui'),
        ('План производства.xlsx', '.'),
        ('Разузловка.xlsx', '.'),
    ],
    hiddenimports=['ortools', 'pyqtgraph', 'openai'],
    hookspath=[], runtime_hooks=[],
    excludes=['tkinter', 'matplotlib'],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [],
          name='Planner',
          debug=False, strip=False, upx=True, console=False)