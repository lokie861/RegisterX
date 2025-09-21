import os
import requests
from packaging import version
import subprocess

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


def download_latest_exe(repo_url: str, version: str, save_dir: str = "temp") -> str:
    """
    Download the latest .exe file from a GitHub repository's latest release.

    Args:
        repo_url (str): GitHub repository URL, e.g., 'https://github.com/owner/repo'
        save_dir (str): Directory to save the .exe file (default: current dir)

    Returns:
        str: Path to the downloaded file, or error message
    """
    try:
        if not os.path.exists(os.path.join(save_dir,"RegisterX.exe")):
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

            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            exe_url = exe_asset["browser_download_url"]
            exe_name = exe_asset["name"]
            save_path = os.path.join(save_dir, exe_name)

            # Download the file
            with requests.get(exe_url, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(save_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            
        updater_path = os.path.join(os.getcwd(),"updater.exe")
        creationflags = subprocess.CREATE_NO_WINDOW
        args = [
                os.path.join(os.getcwd(),"temp","RegisterX.exe"),
                os.path.join(os.getcwd(),"RegisterX.exe"),
                version
        ]

        result = subprocess.run([updater_path] + args, 
                                capture_output=True, 
                                text=True,
                                creationflags=creationflags,
                                timeout=60,
                                check=False,
                                startupinfo = None)
    
    except Exception as e:
        return f"Error: {str(e)}"



def is_update_available(current_version: str, online_version: str) -> bool:
    """
    Compare semantic versions.
    
    Returns True if `current_version` is lower than `online_version`.
    Example:
        is_update_available("1.2.0", "1.3.0")  -> True
        is_update_available("2.0.0", "1.9.9")  -> False
    """
    return version.parse(current_version) < version.parse(online_version)


# print(get_latest_release("https://github.com/lokie861/RegisterX"))
# print(download_latest_exe("https://github.com/lokie861/RegisterX"))
