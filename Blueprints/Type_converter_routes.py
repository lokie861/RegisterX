from flask import Blueprint, render_template, request, jsonify
from Converstion import TypeConversions

typeconverter = Blueprint('typeconverter', __name__)


@typeconverter.route("/")
def typeconverterhome():
    return render_template("typeconvert.html")