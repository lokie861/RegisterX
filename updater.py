import os
import shutil
import sys
import configparser
import subprocess
import time
from pathlib import Path
import platform

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr:
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def get_app_data_dir(app_name: str, create: bool = True) -> Path:
    """
    Return the application data directory for the current OS.
    Creates the directory if it doesn't exist and create=True.

    Args:
        app_name: Name of your application (used as folder).
        create: Whether to create the directory if missing.

    Returns:
        Path object pointing to the application data directory.
    """
    system = platform.system()

    if system == "Windows":
        base = os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
    elif system == "Darwin":  # macOS
        base = Path.home() / "Library" / "Application Support"
    else:  # Linux and others
        base = Path.home() / ".local" / "share"

    app_dir = Path(base) / app_name

    if create:
        app_dir.mkdir(parents=True, exist_ok=True)

    return app_dir


def run_exe(exe_path: str, args: list[str] = None, timeout: int = 60) -> tuple[int, str, str]:
    """
    Run an executable file silently and capture its output.

    Args:
        exe_path (str): Path to the .exe file.
        args (list[str], optional): List of arguments to pass to the exe. Defaults to None.
        timeout (int, optional): Max seconds to wait before killing the process. Defaults to 60.

    Returns:
        tuple[int, str, str]: (exit_code, stdout, stderr)
    """
    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"Executable not found: {exe_path}")

    # Hide cmd window on Windows
    startupinfo = None
    creationflags = 0
    if os.name == "nt":  # Windows only
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        result = subprocess.run(
            [exe_path] + (args if args else []),
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW, 
            text=True,
            timeout=60,
            check=False
        )
        return (result.returncode, result.stdout.strip(), result.stderr.strip())

    except subprocess.TimeoutExpired:
        return (-1, "", f"Process timed out after {timeout} seconds")
    except Exception as e:
        return (-1, "", f"Unexpected error: {e}")


def delete_folder(folder_path: str):
    """
    Delete a folder and all its contents safely.
    """
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"✅ Folder deleted: {folder_path}")
        except Exception as e:
            print(f"⚠️ Failed to delete folder {folder_path}: {e}")
    else:
        print(f"⚠️ Folder does not exist: {folder_path}")


def kill_application(app_name: str):
    """
    Kill all instances of a running application by its executable name.
    """
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/IM", app_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False  # Prevent exceptions if process not running
        )

        # Check if taskkill actually found the process
        if "SUCCESS" in result.stdout.upper():
            print(f"{app_name} terminated successfully.")
        else:
            print(f"{app_name} was not running.")

    except Exception as e:
        # Fallback for any unexpected error
        print(f"Error attempting to terminate {app_name}: {e}")


# def write_ini_value(file_path: str, section: str, key: str, value: str):
#     """
#     Write a key-value pair to an INI file. Creates section if it doesn't exist.
#     """
#     config = configparser.ConfigParser()

#     # Read existing file if it exists
#     if os.path.exists(file_path):
#         config.read(file_path)

#     # Add section if missing
#     if not config.has_section(section):
#         config.add_section(section)

#     # Set the value
#     config.set(section, key, value)

#     # Write changes back to file
#     with open(file_path, 'w', encoding="utf-8") as configfile:
#         config.write(configfile)

#     print(f"✅ Set [{section}] {key} = {value} in {file_path}")


# def replace_exe(new_exe_path: str, target_exe_path: str, ini_path: str, new_version: str, backup: bool = True) -> bool:
#     """
#     Replace an existing exe with a new one.
#     """
#     if not os.path.exists(new_exe_path):
#         print(f"❌ New exe not found: {new_exe_path}")
#         return False

#     if os.path.exists(target_exe_path):
#         if backup:
#             backup_path = target_exe_path + ".bak"
#             shutil.copy2(target_exe_path, backup_path)
#             print(f"📦 Backup created at: {backup_path}")

#         os.remove(target_exe_path)
#         print(f"🗑️ Removed old exe: {target_exe_path}")

#     shutil.copy2(new_exe_path, target_exe_path)
#     print(f"✅ Replaced with new exe: {target_exe_path}")
#     return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_exe.py <installer_path>")
        sys.exit(1)

    new_installer_path = sys.argv[1]

    # Kill Applications
    kill_application("RegisterX.exe")
    time.sleep(5)

    # Replace the downloaded Exe
    # success = replace_exe(new_exe, target_exe, os.path.join(os.getcwd(), "app.ini"), new_version, backup=False)

    # If success write the new version to ini
    # if success:
    #     write_ini_value("app.ini", "CONFIG", "version", new_version)

    exit_code, output, error = run_exe(new_installer_path)

    # Check output instead of comparing object
    time.sleep(5)
    app_dir = get_app_data_dir("RegisterX",False)
    # temp_path = os.path.join(os.getcwd(), "temp")

    delete_folder(app_dir)

    sys.exit(0)
