from flask import Blueprint, render_template, request, jsonify
from Converstion import TypeConversions
from ast import literal_eval

typeconverter = Blueprint('typeconverter', __name__)


@typeconverter.route("/")
def typeconverterhome():
    return render_template("typeconvert.html")

converter = TypeConversions()


@typeconverter.route('/convert', methods=['POST'])
def convert_value():
    """
    Convert data between types using TypeConversions.
    IMPROVED: Now supports long64 and ulong64 types!
    
    Expected JSON:
    {
        "from_type": "uint16" | "string" | "float32" | "double" | "int32" | "uint32" | "long64" | "ulong64",
        "to_type": "string" | "uint16" | "float32" | "double" | "int32" | "uint32" | "long64" | "ulong64",
        "value": <string or list of ints>,
        "endian": "little" | "big"
    }
    """
    try:
        data = request.get_json(force=True)

        # === Validate required fields ===
        required = ["from_type", "to_type", "value", "endian"]
        if not all(field in data for field in required):
            return jsonify({"error": "Missing required fields"}), 400

        from_type = data["from_type"].lower()
        to_type = data["to_type"].lower()
        endian = data["endian"].lower()
        inverse = True if endian == "big" else False
        value = data["value"]

        # === Parse input ===
        if from_type == "uint16":
            # Expecting a list of integers
            if isinstance(value, str):
                try:
                    value = literal_eval(value)
                except Exception:
                    return jsonify({"error": "Invalid array format for uint16"}), 400
            if not (isinstance(value, list) and all(isinstance(v, int) for v in value)):
                return jsonify({"error": "value must be a list of integers for uint16"}), 400

        elif from_type in ["float32", "double", "int32", "uint32", "long64", "ulong64"]:
            try:
                if "float" in from_type or "double" in from_type:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                return jsonify({"error": f"Invalid numeric value for {from_type}"}), 400

        elif from_type == "string":
            if not isinstance(value, str):
                return jsonify({"error": "value must be a string"}), 400

        else:
            return jsonify({"error": f"Unsupported from_type: {from_type}"}), 400

        # === Perform conversion ===
        result = None

        if from_type == "uint16":
            # Convert from uint16 → something
            if to_type == "string":
                result = converter.to_string(value, inverse)
            elif to_type == "float32":
                result = converter.to_float32(value, inverse=inverse)
            elif to_type == "double":
                result = converter.to_double64(value, inverse=inverse)
            elif to_type == "int32":
                result = converter.to_int32(value, inverse=inverse)
            elif to_type == "uint32":
                result = converter.to_uint32(value, inverse=inverse)
            elif to_type == "long64":
                result = converter.to_long64(value, inverse=inverse)
            elif to_type == "ulong64":
                result = converter.to_ulong64(value, inverse=inverse)
            else:
                return jsonify({"error": f"Unsupported to_type: {to_type}"}), 400

        elif from_type == "string":
            result = converter.from_string(value, inverse)

        elif from_type == "float32":
            if to_type == "uint16":
                result = converter.from_float32(float(value), inverse)
            else:
                return jsonify({"error": "float32 can only convert to uint16"}), 400

        elif from_type == "double":
            if to_type == "uint16":
                result = converter.from_double64(float(value), inverse)
            else:
                return jsonify({"error": "double can only convert to uint16"}), 400

        elif from_type == "int32":
            if to_type == "uint16":
                result = converter.from_int32(int(value), inverse)
            else:
                return jsonify({"error": "int32 can only convert to uint16"}), 400

        elif from_type == "uint32":
            if to_type == "uint16":
                result = converter.from_uint32(int(value), inverse)
            else:
                return jsonify({"error": "uint32 can only convert to uint16"}), 400

        # NEW: long64 support
        elif from_type == "long64":
            if to_type == "uint16":
                result = converter.from_long64(int(value), inverse)
            else:
                return jsonify({"error": "long64 can only convert to uint16"}), 400

        # NEW: ulong64 support
        elif from_type == "ulong64":
            if to_type == "uint16":
                result = converter.from_ulong64(int(value), inverse)
            else:
                return jsonify({"error": "ulong64 can only convert to uint16"}), 400

        else:
            return jsonify({"error": f"Unsupported conversion: {from_type} → {to_type}"}), 400

        return jsonify({
            "from_type": from_type,
            "to_type": to_type,
            "endian": endian,
            "input": value,
            "result": result
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# Optional: Get supported conversions
@typeconverter.route('/api/supported-types', methods=['GET'])
def get_supported_types():
    """Returns all supported data types for conversion"""
    return jsonify({
        "types": [
            "uint16",
            "string",
            "float32",
            "double",
            "int32",
            "uint32",
            "long64",
            "ulong64"
        ],
        "endian_options": ["little", "big"],
        "conversion_rules": {
            "uint16": ["string", "float32", "double", "int32", "uint32", "long64", "ulong64"],
            "string": ["uint16"],
            "float32": ["uint16"],
            "double": ["uint16"],
            "int32": ["uint16"],
            "uint32": ["uint16"],
            "long64": ["uint16"],
            "ulong64": ["uint16"]
        }
    })