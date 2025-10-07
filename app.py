
import os
import sys
import time
import webbrowser
import ctypes
import signal
import winreg
import threading

from PIL import Image
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS
import pystray

from Blueprints.Converter_routes import convert_blueprint
from Blueprints.Type_converter_routes import typeconverter
from version_control import (
    get_latest_release, 
    is_update_available, 
    start_update_process,
    REPO_DIR,
    BASE_PATH,
    DEBUG_MODE,
    ICON_PATH
    )

APP_SETTINGS = None
icon = None
LOCK_FILE = "RegisterX.lock"
VERSION = "0.0.0"
CONFIG = {}


def read_registerx_config():
    config = {}
    try:
        # Open the registry key where RegisterX settings are stored
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\RegisterX"
        )

        # Enumerate all values under this key
        i = 0
        while True:
            try:
                name, val, regtype = winreg.EnumValue(key, i)

                # Convert registry strings like "true"/"false" to bool
                if isinstance(val, str):
                    if val.lower() in ("true", "false"):
                        val = val.lower() == "true"
                    elif val.isdigit():
                        val = int(val)

                config[name] = val
                i += 1
            except OSError:
                break  # No more values

        winreg.CloseKey(key)

    except FileNotFoundError:
        print("RegisterX registry key not found.")
        return None

    return config


def ensure_single_instance():
    global icon
    """Ensure only one instance of RegisterX.exe is running using Windows mutex."""
    try:
        mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "RegisterX_SingleInstanceMutex")
        last_error = ctypes.windll.kernel32.GetLastError()

        # ERROR_ALREADY_EXISTS = 183
        if last_error == 183:
            print("❌ Another instance of RegisterX.exe is already running.")
            # on_notify(icon=icon,item=None,title="RegisterX",message="Another instance is running.")
            sys.exit(1)
    except Exception as e:
        print(f"Error creating mutex: {e}")
        # on_notify(icon=icon,item=None,title="RegisterX",message="Another instance is running.")
        sys.exit(1)


def update_application():
    print("updating application...")
    threading.Thread(target=start_update_process,args=(VERSION,)).start()



# -----------------------------
# System tray integration
# -----------------------------

def stop_flask():
    pid = os.getpid()
    on_notify(icon=icon,item=None,title="RegisterX",message="Stopping RegisterX")
    time.sleep(5)
    print(f"Stopping Flask server (PID {pid})...")
    os.kill(pid, signal.SIGTERM)  # or SIGINT


def run_tray():
    global icon, VERSION, ICON_PATH, CONFIG, REPO_DIR
    """Set up and run the system tray icon."""
    if icon is not None:
        return  # Already running

    try:
        release_details = get_latest_release(REPO_DIR)
        release_available = is_update_available(
            CONFIG.get("version","0.0.0"),
            release_details.get("name")[1:]
        )
        if release_available:
            VERSION = release_details.get("name")[1:]
    except Exception as e:
        print(f"Error checking for updates: {e}")
        release_available = False

    image = Image.open(ICON_PATH)
    menu = pystray.Menu(
        pystray.MenuItem("Open RegisterX", open_app, enabled=True),
        pystray.MenuItem("Exit", stop_app, enabled=True),
        pystray.MenuItem("Update Application", update_application, enabled=release_available)
    )

    icon = pystray.Icon("RegisterX", image, "RegisterX", menu)

    # Run the tray icon in its own thread to avoid blocking
    tray_thread = threading.Thread(target=icon.run)
    tray_thread.daemon = True
    tray_thread.start()


def stop_app(item):
    global icon
    icon.stop()
    stop_flask()


def on_notify(icon, item, title, message):
    global ICON_PATH
    """Display a system notification."""
    icon.notify(title=title, message=message)


def open_app(icon, item):
    host = "127.0.0.1" if CONFIG.get("host","127.0.0.1") == "0.0.0.0" else CONFIG.get("host","127.0.0.1")
    webbrowser.open(f'http://{host}:{CONFIG.get("port",5000)}')

def create_tray():
    tray = threading.Thread(target=run_tray)
    tray.daemon = True
    tray.start()

# -----------------------------
# Flask App setup
# -----------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'RegisterX'
CORS(app, supports_credentials=True)
app.register_blueprint(convert_blueprint,url_prefix="/convert")
app.register_blueprint(typeconverter,url_prefix="/typeconverter")


# -----------------------------
# Default route
# -----------------------------

@app.route("/")
def index():
    return redirect("/home")


@app.route("/exit")
def exit_app():
    sys.exit(0)


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        bug_report = request.form.get("bug_report")
        # Here you can handle sending email
        # For example using Flask-Mail or smtplib
        # For now, just print (or log) it
        print("Bug report received:", bug_report)
        return redirect(url_for("about"))
    
    return render_template("about.html")


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
        
if __name__ == '__main__':
    # Read configuration from the registry
    CONFIG = read_registerx_config()

    port=int(CONFIG.get("port",5000))

    if DEBUG_MODE is None:
        debug_mode = CONFIG.get("debug",False)
    else:
        debug_mode = False

    if not debug_mode:
        ensure_single_instance()

    if CONFIG.get("run_systray",""):
        create_tray()
        print("Started systray...")
    else:
        print("Systray disabled in settings.")

    time.sleep(5)

    

    on_notify(icon=icon,item=None,title="RegisterX",message=f"Started RegisterX service on port {port}")
    
    # Starts the Flask App
    app.run(host=CONFIG.get("host","0.0.0.0"),
            port=port,
            debug=debug_mode)
