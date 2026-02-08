from flask import Blueprint, render_template, request, jsonify
import Convert

convert_blueprint = Blueprint('convert', __name__)


@convert_blueprint.route("/")
def convert_page():
    plc_make_list = list(Convert.PLC_MAPPINGS.keys())  
    plc_type_list = {}
    for make in Convert.PLC_MAPPINGS.keys():
        plc_type_list[make] = list(Convert.PLC_MAPPINGS[make].keys())
    return render_template("convert.html", plc_make=plc_make_list, plc_mappings=plc_type_list)


@convert_blueprint.route("/api/convert", methods=["GET"])
def convert_api():
    """
    IMPROVED VERSION: Uses generic converter instead of if-elif chain.
    This makes it easy to add new PLC types - just add to PLC_MAPPINGS!
    """
    plc_make = request.args.get("make", "Delta")  # Default to Delta
    plc_type = request.args.get("plc")
    address = request.args.get("address")
    reg_type = request.args.get("regtype")

    # Validate inputs
    if not all([plc_type, address, reg_type]):
        return jsonify({
            "error": "Missing required parameters: plc, address, regtype"
        }), 400

    try:
        # Use the new generic converter function
        raw, converted = Convert.convert_plc_address(plc_make, plc_type, address, reg_type)
        
        # Check for error messages
        if "Unsupported" in raw or "Invalid" in raw:
            return jsonify({
                "error": raw,
                "raw": raw,
                "converted": converted
            }), 400

        return jsonify({
            "raw": raw,
            "converted": converted,
            "plc_make": plc_make,
            "plc_type": plc_type,
            "address": address,
            "reg_type": reg_type
        })

    except Exception as e:
        print(f"Error during conversion: {e}")
        return jsonify({
            "error": f"Conversion failed: {str(e)}"
        }), 500


# Optional: Endpoint to get available PLC types
@convert_blueprint.route("/api/plc-types", methods=["GET"])
def get_plc_types():
    """Returns all available PLC manufacturers and models"""
    return jsonify({
        "manufacturers": list(Convert.PLC_MAPPINGS.keys()),
        "models": Convert.PLC_MAPPINGS
    })


# Optional: Endpoint to get register types for a specific model
@convert_blueprint.route("/api/register-types", methods=["GET"])
def get_register_types():
    """Returns available register types for a specific PLC model"""
    plc_make = request.args.get("make", "Delta")
    plc_model = request.args.get("model")
    
    if not plc_model:
        return jsonify({"error": "Missing model parameter"}), 400
    
    if plc_make not in Convert.PLC_MAPPINGS:
        return jsonify({"error": f"Unknown manufacturer: {plc_make}"}), 404
    
    if plc_model not in Convert.PLC_MAPPINGS[plc_make]:
        return jsonify({"error": f"Unknown model: {plc_model}"}), 404
    
    model_data = Convert.PLC_MAPPINGS[plc_make][plc_model]
    
    # Extract register types and their supported address types
    register_info = {}
    for reg_type, addr_types in model_data.items():
        register_info[reg_type] = list(addr_types.keys())
    
    return jsonify({
        "make": plc_make,
        "model": plc_model,
        "registers": register_info
    })