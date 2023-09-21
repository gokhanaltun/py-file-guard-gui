import subprocess
import shutil

desktop_file = """
[Desktop Entry]
Name=Py-File-Guard-GUI
Exec=python3 /opt/py-file-guard-gui/pfg.py
Icon=/opt/py-file-guard-gui/icon.png
Terminal=false
Type=Application
Categories=Utility;
"""

with open("pfg.desktop", "w") as f:
    f.write(desktop_file)

shutil.move("pfg.desktop", "/usr/share/applications/")


def ignore_files_and_folders(path, files):
    ignore_list = ['.idea', 'install.py', 'requirements.txt']
    return [item for item in files if item in ignore_list]


shutil.copytree("../py-file-guard-gui", "/opt/py-file-guard-gui", ignore=ignore_files_and_folders)

subprocess.run(["sudo", "update-desktop-database"])

print("Complete")
