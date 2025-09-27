
import os
import sys
from threading import Thread
import time
import webbrowser
import configparser
import msvcrt
import signal
from plyer import notification

from threading import Thread
from PIL import Image
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS
import pystray

from Blueprints.Converter_routes import convert_blueprint
from version_control import (
    get_latest_release, 
    is_update_available, 
    start_update_process,
    REPO_DIR,
    BASE_PATH,
    DEBUG_MODE
    )

APP_SETTINGS = None
ICON_PATH = None
icon = None
LOCK_FILE = "RegisterX.lock"
VERSION = "0.0.0"




def load_app_settings(file_path: str) -> dict:
    """
    Reads an INI file and converts it into a nested dictionary.
    
    :param file_path: Path to the ini file
    :return: Dictionary with sections as keys and their key-value pairs as nested dicts
    """
    config = configparser.ConfigParser()
    config.optionxform = str  # preserve case sensitivity of keys
    config.read(file_path)

    ini_dict = {section: dict(config[section]) for section in config.sections()}
    print("App Settings Loaded")
    return ini_dict


APP_SETTINGS = load_app_settings(os.path.join(os.getcwd(),"app.ini"))
CONFIG = APP_SETTINGS.get("CONFIG",{})

ICON_PATH = os.path.join(BASE_PATH, "static", "logo", "RegisterX.ico")



def send_notification(title: str, message: str, timeout: int = 5):
    icon_path = os.path.join(ICON_PATH)
    notification.notify(
        title=title,
        message=message,
        timeout=timeout,
        app_icon=icon_path
    )

def ensure_single_instance():
    """Prevent running multiple instances of the same app on Windows."""
    global lockfile
    lockfile = open(LOCK_FILE, "w")
    try:
        msvcrt.locking(lockfile.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        print("❌ Another instance of this Flask app is already running.")
        send_notification("RegisterX","Another Instance is running.",timeout=2)
        sys.exit(1)

def update_application():
    print("updating application...")
    Thread(target=start_update_process,args=(VERSION,)).start()

# -----------------------------
# System tray integration
# -----------------------------

def stop_flask():
    pid = os.getpid()
    send_notification("RegisterX","Stopping RegisterX",timeout=5)
    time.sleep(5)
    print(f"Stopping Flask server (PID {pid})...")
    os.kill(pid, signal.SIGTERM)  # or SIGINT
    sys.exit(0)



def run_tray():
    global icon, VERSION
    if icon is None:
        try:
            release_details = get_latest_release(REPO_DIR)
            release_available = is_update_available(
                                    CONFIG.get("version","0.0.0"),
                                    release_details.get("name")[1:])
            if release_available:
                VERSION = release_details.get("name")[1:]
        except Exception as e:
            print(f"Error checking for updates: {e}")
            release_available = False

        image = Image.open(ICON_PATH)
        menu = pystray.Menu(
            pystray.MenuItem("Open RegisterX", open_app,enabled=True),
            pystray.MenuItem("Exit", stop_app,enabled=True),
            pystray.MenuItem("Update Application",update_application,enabled=release_available)
        )

        icon = pystray.Icon("RegisterX", image, "RegisterX", menu)
        icon.run()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        if icon:
            icon.stop()


def create_tray():
    tray = Thread(target=run_tray)
    tray.daemon = True
    tray.start()


def stop_app(icon, item):
    stop_flask()
    icon.stop()
    sys.exit(1)


def open_app(icon, item):
    host = "127.0.0.1" if CONFIG.get("host","127.0.0.1") == "0.0.0.0" else CONFIG.get("host","127.0.0.1")
    webbrowser.open(f'http://{host}:{CONFIG.get("port",5000)}')



# -----------------------------
# Flask App setup
# -----------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'RegisterX'
CORS(app, supports_credentials=True)


app.register_blueprint(convert_blueprint,url_prefix="/convert")

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


        
if __name__ == '__main__':
    port=int(CONFIG.get("port",5000))
    if DEBUG_MODE is None:
        debug_mode = CONFIG.get("debug","false").lower() == "true"
    else:
        debug_mode = False

    if not debug_mode:
        ensure_single_instance()

    if CONFIG.get("run_systray",""):
        create_tray()
        print("Started systray...")
    else:
        print("Systray disabled in settings.")
    
    send_notification("RegisterX",f"Started RegisterX service on port {port}",timeout=2)
    app.run(host=CONFIG.get("host","0.0.0.0"),
            port=port,
            debug=debug_mode)
