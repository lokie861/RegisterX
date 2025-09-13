import os
import subprocess
import sys
import shutil

# === Configuration ===
project_dir = os.getcwd()
icon_path = os.path.join(project_dir, "logo\\plc_to_modbus.ico")
entry_file = os.path.join(project_dir, "app.py")
exe_name = "PLC Reg to Modbus Converter"
exe_output_dir = os.path.join(os.getcwd(), "Builds","EXE")

output_dir = os.path.join(project_dir, "Builds", "Installer")
iscc_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"  # Adjust path if needed


def build_exe():
    command = (
        f'pyinstaller --noconfirm --onefile --console '
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

        # Collect submodules for packages that use dynamic imports
        f'--collect-submodules engineio '
        f'--collect-submodules werkzeug '


        # Data files
        f'--add-data "{project_dir}/Convert.py;." '
        f'--add-data "{project_dir}/Blueprints;Blueprints" '
        f'--add-data "{project_dir}/templates;templates" '
        f'--add-data "{project_dir}/static;static" '
        f'--add-data "{project_dir}/logo;logo" '

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
        paths = ['Backend-Builds', 'dist', 'build']
    elif type == 'installer':
        paths = ['Builds']
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
    if len(sys.argv) > 3 or not (sys.argv[1] in ("clean", "exe", "installer")):
        print("Usage: python build.py [exe|installer|clean]")
        return

    if sys.argv[1] == "exe":
        build_exe()
    elif sys.argv[1] == "installer":
        build_installer()
    elif sys.argv[1] == "clean":
        clean_builds(sys.argv[2])
    else:
        print("invalid parameter")


if __name__ == "__main__":
    main()
