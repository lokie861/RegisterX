from flask import Blueprint, render_template, request, jsonify
import Convert

convert_blueprint = Blueprint('convert', __name__)





@convert_blueprint.route("/")
def convert_page():
    plc_keys = list(Convert.PLC_MAPPINGS.keys())
    return render_template("convert.html",plc_keys=plc_keys)








@convert_blueprint.route("/api/convert",methods=["GET"])
def convert_api():
    plc_type = request.args.get("plc")
    address = request.args.get("address")
    reg_type = request.args.get("regtype")

    try:
        # Example: call the real converter
        if plc_type == "SV2":
            raw, converted = Convert.sv2(address, reg_type)
        elif plc_type == "AS":
            raw, converted = Convert.as_series(address, reg_type)
        elif plc_type == "SA2":
            raw, converted = Convert.sa2(address, reg_type)
        elif plc_type == "SS2":
            raw, converted = Convert.ss2(address, reg_type)
        else:
            raw, converted = ("99999", "999")

        return jsonify({"raw": raw, "converted": converted})

    except Exception as e:
        print(f"Error during conversion: {e}")
        return jsonify({"error": str(e)}), 400
