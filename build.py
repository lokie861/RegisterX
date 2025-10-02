import os
import subprocess
import sys
import shutil

# === Configuration ===
project_dir = os.getcwd()
icon_path = os.path.join(project_dir, "static\\logo\\RegisterX.ico")
entry_file = os.path.join(project_dir, "app.py")
exe_name = "RegisterX"
exe_output_dir = os.path.join(os.getcwd(), "Builds","EXE")

output_dir = os.path.join(project_dir, "Builds", "Installer")
iscc_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"  # Adjust path if needed


def build_updater():
    updater_script = os.path.join(project_dir, "updater.py")
    updater_output_dir = os.path.join(os.getcwd(), "Builds","Updater")
    command = (
        f'pyinstaller --noconfirm --onefile --noconsole '
        f'--distpath "{exe_output_dir}" '
        f'--name "updater" '
        f'--icon "{icon_path}" '
        f'"{updater_script}" '
    )

    print("[INFO] Building Updater EXE...")
    subprocess.run(command, shell=True, check=True)
    print("[SUCCESS] Updater EXE created.")

def build_exe():
    command = (
        f'pyinstaller --noconfirm --onefile --noconsole '
        f'--manifest elevated.manifest --distpath "{exe_output_dir}" '
        f'--name "{exe_name}" '
        f'--icon "{icon_path}" '

        # Core hidden imports
        f'--hidden-import=flask '
        f'--hidden-import=socketio.namespace '
        f'--hidden-import=engineio.async_drivers.threading '
        f'--hidden-import=flask_cors '
        f'--hidden-import=PIL.Image '
        f'--hidden-import=pystray '
        f'--hidden-import=bidict '
        f'--hidden-import=flask_session '
        f'--hidden-import=cachelib '
        f'--hidden-import=wmi '
        f'--hidden-import=pywintypes '
        f'--hidden-import=plyer '
        f'--hidden-import=ctypes '

        # Collect submodules for packages that use dynamic imports
        f'--collect-submodules engineio '
        f'--collect-submodules werkzeug '
        f'--collect-submodules plyer '


        # Data files
        f'--add-data "{project_dir}/Convert.py;." '
        f'--add-data "{project_dir}/Blueprints;Blueprints" '
        f'--add-data "{project_dir}/templates;templates" '
        f'--add-data "{project_dir}/static;static" '

        f'"{entry_file}" '
    )

    print("[INFO] Running PyInstaller...")
    subprocess.run(command, shell=True, check=True)
    print("[SUCCESS] EXE created.")


def build_installer():
    exe_path = os.path.abspath(f"dist\\{exe_name}.exe")
    iss_script = "Builder.iss"
    print("[INFO] Running Inno Setup...")
    subprocess.run([iscc_path, iss_script], check=True)
    print(f"[SUCCESS] Installer created in: {output_dir}")


def clean_builds(type):
    if type == 'exe':
        paths = ['Builds\EXE', 'builds',"build"]
    elif type == 'installer':
        paths = ['Builds\Installer']
    else:
        paths = []

    for path in paths:
        path = os.path.abspath(path)
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print(f"Deleted folder: {path}")
            except PermissionError:
                print(f"Permission denied: {path} (try running as admin)")
            except Exception as e:
                print(f"Error deleting folder {path}: {e}")
        else:
            print(f"Folder not found: {path}")


def main():
    if len(sys.argv) > 4 or not (sys.argv[1] in ("clean", "exe", "installer", "updater","all")):
        print("Usage: python build.py [exe|installer|clean]")
        return

    if sys.argv[1] == "exe":
        build_exe()
    elif sys.argv[1] == "installer":
        build_installer()
    elif sys.argv[1] == "updater":
        build_updater()
    elif sys.argv[1] == "clean":
        clean_builds(sys.argv[2])
    elif sys.argv[1] == "all":
        clean_builds('exe')
        build_exe()
        build_updater()
        build_installer()
    else:
        print("invalid parameter")


if __name__ == "__main__":
    main()
