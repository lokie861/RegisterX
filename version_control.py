import os
import sys
import requests
from packaging import version
import subprocess
import hashlib
from pathlib import Path
import platform
import shutil
from plyer import notification

BASE_PATH = None
DEBUG_MODE = None

if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    BASE_PATH = sys._MEIPASS
    DEBUG_MODE = False
else:
    # Running as script or unpacked/
    BASE_PATH = os.getcwd()

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # hide window


REPO_DIR = "https://github.com/lokie861/RegisterX"
ICON_PATH = os.path.join(BASE_PATH, "static", "logo", "RegisterX.ico")


def send_notification(title: str, message: str, timeout: int = 5):
    icon_path = os.path.join(ICON_PATH)
    notification.notify(
        title=title,
        message=message,
        timeout=timeout,
        app_icon=icon_path
    )


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


def load_hashes(filepath: str):
    """Load file -> return dict {name: sha}"""
    hashes = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            name, sha = line.split(":", 1)
            hashes[name.strip()] = sha.strip()
    return hashes


def get_sha_by_name(name:str , filepath:str):
    """Get SHA for given file name"""
    hashes = load_hashes(filepath)
    return hashes.get(name)


def get_latest_release(repo_url: str) -> dict:
    """
    Fetch the latest release information from a GitHub repository.

    Args:
        repo_url (str): GitHub repository URL, e.g., 'https://github.com/owner/repo'

    Returns:
        dict: Release information (tag name, name, published date, url), or error message.
    """
    try:
        # Extract owner and repo from URL
        parts = repo_url.rstrip('/').split('/')
        if len(parts) < 2:
            return {"error": "Invalid repository URL"}
        
        owner, repo = parts[-2], parts[-1]

        # GitHub API URL
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

        response = requests.get(api_url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return {
                "tag_name": data.get("tag_name"),
                "name": data.get("name"),
                "published_at": data.get("published_at"),
                "html_url": data.get("html_url"),
            }
        elif response.status_code == 404:
            return {"error": "No releases found for this repository"}
        else:
            return {"error": f"Failed to fetch release info (status {response.status_code})"}

    except Exception as e:
        return {"error": str(e)}


def download_checksum_file(repo_url: str, save_dir: str = "temp"):
    # Extract owner and repo
    try:
        parts = repo_url.rstrip('/').split('/')
        if len(parts) < 2:
            return "Invalid repository URL"
        
        owner, repo = parts[-2], parts[-1]

        # GitHub API URL
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        response = requests.get(api_url, timeout=15)

        if response.status_code != 200:
            return f"Failed to fetch release info (status {response.status_code})"

        data = response.json()

        # Look for .txt assets
        assets = data.get("assets", [])
        txt_assets = next((a for a in assets if a["name"].endswith(".txt")), None)
        if not txt_assets:
            return "No .txt file found in the latest release"

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        txt_url = txt_assets["browser_download_url"]
        txt_name = txt_assets["name"]
        save_path = os.path.join(save_dir, txt_name)

        # Download the file
        with requests.get(txt_url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return save_path
    
    except Exception as e:
        return None


def get_file_hash_with_certutil(path: str | Path, algorithm: str = "SHA256") -> str:
    """
    Use Windows' certutil to compute a file hash.
    algorithm: MD5, SHA1, SHA256, SHA384, SHA512 (case-insensitive)
    Returns: hex digest (lowercase)
    Raises: FileNotFoundError, RuntimeError
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")

    alg = algorithm.upper()
    # certutil expects algorithms like SHA256, MD5, etc.
    cmd = ["certutil", "-hashfile", str(p), alg]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError as e:
        # certutil not found (very unlikely on Windows)
        raise RuntimeError("certutil not available on this system") from e

    out = proc.stdout.strip()
    if proc.returncode != 0:
        # include stderr for debugging
        raise RuntimeError(f"certutil failed: returncode={proc.returncode}\n{proc.stderr.strip()}")

    # certutil output example:
    # SHA256 hash of file C:\path\to\file.exe:
    # aa 11 bb 22 ... (bytes separated by spaces)
    # CertUtil: -hashfile command completed successfully.
    #
    # We'll extract the first long hex-like line from the output.
    for line in out.splitlines():
        line = line.strip()
        # skip header/footer lines
        if not line:
            continue
        # a valid hex line will be mostly hex chars and spaces and length >= 32 (for SHA256)
        cleaned = line.replace(" ", "")
        if all(c in "0123456789abcdefABCDEF" for c in cleaned) and len(cleaned) >= 32:
            return cleaned.lower()

    raise RuntimeError(f"Could not parse certutil output:\n{out}")


def compute_file_hash_python(path: str | Path, algorithm: str = "sha256") -> str:
    """
    Pure-Python file hash. algorithm names follow hashlib (sha1, sha256, md5, etc.)
    Returns: hex digest (lowercase)
    Raises: FileNotFoundError, ValueError
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")

    alg = algorithm.lower()
    try:
        hasher = hashlib.new(alg)
    except Exception as e:
        raise ValueError(f"Unsupported algorithm: {algorithm}") from e

    CHUNK = 8192
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            hasher.update(chunk)
    return hasher.hexdigest().lower()


def get_hash(path: str | Path, algorithm: str = "sha256", prefer_certutil: bool = True) -> str:
    """
    Try certutil first (Windows), otherwise fallback to Python implementation.
    algorithm is case-insensitive (SHA256 or sha256).
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")

    if prefer_certutil:
        try:
            # certutil expects algorithms like SHA256
            return get_file_hash_with_certutil(p, algorithm.upper())
        except Exception:
            # fallback silently to pure-Python
            pass

    # fallback: map algorithm name to hashlib style
    return compute_file_hash_python(p, algorithm)


def get_release_checksum(repo_url: str, filename: str) -> str:
    checksum_path = download_checksum_file(repo_url=repo_url)
    release_hash = get_sha_by_name("RegisterX_Installer.exe",checksum_path)
    downloaded_hash = get_hash(os.path.join("temp","RegisterX_Installer.exe"), algorithm="sha256", prefer_certutil=True)
    if release_hash == downloaded_hash:
        pass
    else:
        pass


def download_latest_exe(repo_url: str, version: str, save_dir: str) -> str:
    """
    Download the latest .exe file from a GitHub repository's latest release.

    Args:
        repo_url (str): GitHub repository URL, e.g., 'https://github.com/owner/repo'
        save_dir (str): Directory to save the .exe file (default: current dir)

    Returns:
        str: Path to the downloaded file, or error message
    """

    try:
        
        if os.path.exists(os.path.join(save_dir,"RegisterX_Installer.exe")):
            pass
        else: 
            # Extract owner and repo
            parts = repo_url.rstrip('/').split('/')
            if len(parts) < 2:
                return "Invalid repository URL"
            
            owner, repo = parts[-2], parts[-1]

            # GitHub API URL
            api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
            response = requests.get(api_url, timeout=15)

            if response.status_code != 200:
                return f"Failed to fetch release info (status {response.status_code})"

            data = response.json()

            # Look for .exe assets
            assets = data.get("assets", [])
            exe_asset = next((a for a in assets if a["name"].endswith(".exe")), None)

            if not exe_asset:
                return "No .exe file found in the latest release"
            print(exe_asset)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            exe_url = exe_asset["browser_download_url"]
            exe_name = "RegisterX_Installer.exe"
            save_path = os.path.join(save_dir, exe_name)

            # Download the file
            with requests.get(exe_url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(save_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

        return save_path
    
    except Exception as e:
        return None


def is_update_available(current_version: str, online_version: str) -> bool:
    """
    Compare semantic versions.
    
    Returns True if `current_version` is lower than `online_version`.
    Example:
        is_update_available("1.2.0", "1.3.0")  -> True
        is_update_available("2.0.0", "1.9.9")  -> False
    """
    return version.parse(current_version) < version.parse(online_version)



def start_update_process(new_version: str):
    
    global REPO_DIR
    
    print("Creating AppData directory...")
    appdata_dir = get_app_data_dir("RegisterX", create=False)

    if os.path.exists(os.path.join(appdata_dir,"RegisterX_Installer.exe")):
        delete_folder(appdata_dir)
        appdata_dir = get_app_data_dir("RegisterX", create=True)

    print("Downloading checksum file...")
    checksum_path = download_checksum_file(repo_url=REPO_DIR, save_dir=appdata_dir)
    if checksum_path is None:
        print("Failed to download checksum file.")
        send_notification("RegisterX","Failed to download updates\nTry again later",timeout=5)
        delete_folder(appdata_dir)
        return
    
    print("Downloading latest installer...")  # Fixed typo: "Installler" -> "installer"
    new_installer_path = download_latest_exe(repo_url=REPO_DIR,version=new_version,save_dir=appdata_dir)
    if new_installer_path is None:
        print("Failed to download the latest executable.")
        send_notification("RegisterX","Failed to download updates\nTry again later",timeout=5)
        delete_folder(appdata_dir)
        return
    
    # BUG FIX: Verify downloaded version matches expected version
    print("Verifying version...")
    release_info = get_latest_release(REPO_DIR)
    actual_version = release_info.get("name", "").lstrip("v")
    if actual_version != new_version:
        print(f"Version mismatch! Expected {new_version}, got {actual_version}")
        send_notification("RegisterX", "Update version mismatch", timeout=5)
        delete_folder(appdata_dir)
        return
    
    print("Verifying checksum...")
    release_hash = get_sha_by_name("RegisterX_Installer.exe",checksum_path)
    if release_hash is None:
        send_notification("RegisterX","Downloaded hash verification failed\nTry again later",timeout=5)  # Fixed typo: "varification" -> "verification"
        delete_folder(appdata_dir)
        return
    
    try:
        print("Computing hash of downloaded file...")
        downloaded_hash = get_hash(new_installer_path, algorithm="sha256", prefer_certutil=True)
        print(f"Release hash: {release_hash}")
        print(f"Downloaded hash: {downloaded_hash}")
        
        # BUG FIX #1: Case-insensitive hash comparison
        if release_hash.lower() == downloaded_hash.lower():
            print("Hash verified. Update can proceed.")
            updater_path = os.path.join(os.getcwd(),"updater.exe")
            args = [new_installer_path]

            # Create startup info to hide window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            print(f"Running updater: {updater_path} with args {args}")
            result = subprocess.run(
                            [updater_path] + args,
                            creationflags=subprocess.CREATE_NO_WINDOW,  # prevent cmd window
                            capture_output=True,
                            text=True,
                            timeout=120,  # Increased timeout from 60 to 120
                            check=False
                        )
            
            # Note: Control won't return here if updater kills this process
            
        else:
            # BUG FIX #2: Proper error handling for hash mismatch
            print("Hash mismatch! Update aborted.")
            print(f"Expected: {release_hash}")
            print(f"Got: {downloaded_hash}")
            send_notification("RegisterX", "Update verification failed - hash mismatch", timeout=5)
            delete_folder(appdata_dir)
            return
            
    except Exception as e:
        # BUG FIX #3: Notify user of exceptions
        print(f"Error during update: {e}")
        send_notification("RegisterX", f"Update failed: {str(e)}", timeout=5)
        delete_folder(appdata_dir)
        return

# get_release_checksum("https://github.com/lokie861/RegisterX","checksum.txt")
# print(download_latest_exe("https://github.com/lokie861/RegisterX"))
# download_latest_exe("https://github.com/lokie861/RegisterX","0.0.0")

# start_update_process("0.0.0")