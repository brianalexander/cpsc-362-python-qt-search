#Code to make it executable
#FROM: https://stackoverflow.com/questions/41570359/how-can-i-convert-a-py-to-exe-for-python


from cx_Freeze import setup, Executable

base = None    

executables = [Executable("mainwindow.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Searchy",
    options = options,
    version = "1.0",
    description = 'Search app for search enthusiasts',
    executables = executables
)