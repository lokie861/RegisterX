
import os
import sys
from threading import Thread
import time
import webbrowser
import configparser

from PIL import Image
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS
import pystray

from Blueprints.Converter_routes import convert_blueprint



BASE_PATH = None 
APP_SETTINGS = None
ICON_PATH = None
icon = None

# -----------------------------
# Path setup
# -----------------------------
# BASE_PATH = getattr(sys, 'frozen', False) and sys._MEIPASS or os.getcwd()

if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    BASE_PATH = sys._MEIPASS
else:
    # Running as script or unpacked/
    BASE_PATH = os.getcwd()



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

ICON_PATH = os.path.join(BASE_PATH, "logo", "plc_to_modbus.ico")

# -----------------------------
# System tray integration
# -----------------------------
def run_tray():
    global icon
    if icon is None:
        image = Image.open(ICON_PATH)
        menu = pystray.Menu(
            pystray.MenuItem("Open Address Converter", open_app),
            pystray.MenuItem("Exit", stop_app)
        )
        icon = pystray.Icon("PLC to Modbus", image, "PLC to Modbus", menu)
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
    icon.stop()
    os._exit(0)


def open_app(icon, item):
    host = "127.0.0.1" if CONFIG.get("host","127.0.0.1") == "0.0.0.0" else CONFIG.get("host","127.0.0.1")
    webbrowser.open(f'http://{host}:{CONFIG.get("port",5000)}')


# -----------------------------
# Flask App setup
# -----------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'PLCTOMODBUS'
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
    os._exit(0)


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
    print(CONFIG)
    if CONFIG.get("run_systray",""):
        create_tray()
        print("Started systray...")
    else:
        print("Systray disabled in settings.")

    app.run(host=CONFIG.get("host","0.0.0.0"),
            port=CONFIG.get("port",5000),
            debug=CONFIG.get("debug","false").lower() == "true"
    )
