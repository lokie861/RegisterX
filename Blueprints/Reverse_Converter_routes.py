from flask import Blueprint, render_template, request, jsonify
import Reverse_Convert

reverse_convert_blueprint = Blueprint('reverse_convert', __name__)


@reverse_convert_blueprint.route("/")
def reverse_convert_page():
    """Render the reverse conversion page"""
    plc_make_list = list(Reverse_Convert.PLC_MAPPINGS.keys())  
    plc_type_list = {}
    for make in Reverse_Convert.PLC_MAPPINGS.keys():
        plc_type_list[make] = list(Reverse_Convert.PLC_MAPPINGS[make].keys())
    return render_template("reverse_convert.html", plc_make=plc_make_list, plc_mappings=plc_type_list)


@reverse_convert_blueprint.route("/api/reverse-convert", methods=["GET"])
def reverse_convert_api():
    """
    API endpoint for reverse conversion (Modbus → PLC address)
    
    Query Parameters:
        - make: PLC manufacturer (default: "Delta")
        - plc: PLC model (e.g., "SV2", "ES2", "AS")
        - address: Modbus address (raw or processed)
        - regtype: "bit" or "word" (optional - if not provided, returns all matches)
    
    Returns:
        JSON with plc_address and description
    """
    plc_make = request.args.get("make", "Delta")
    plc_type = request.args.get("plc")
    modbus_address = request.args.get("address")
    reg_type = request.args.get("regtype")  # Can be None

    # Validate inputs
    if not plc_type or not modbus_address:
        return jsonify({
            "error": "Missing required parameters: plc and address"
        }), 400

    try:
        # If regtype is specified, do single conversion
        if reg_type:
            plc_addr, description = Reverse_Convert.modbus_to_plc(
                plc_make, plc_type, modbus_address, reg_type
            )
            
            # Check for error messages
            if any(err in plc_addr for err in ["Unsupported", "Invalid", "Not Found"]):
                return jsonify({
                    "error": plc_addr,
                    "description": description
                }), 400

            return jsonify({
                "plc_address": plc_addr,
                "description": description,
                "modbus_address": modbus_address,
                "addr_type": reg_type,
                "plc_make": plc_make,
                "plc_type": plc_type
            })
        
        # If regtype not specified, find all possible matches
        else:
            results = Reverse_Convert.find_all_possible_plc_addresses(
                plc_make, plc_type, modbus_address
            )
            
            if not results:
                return jsonify({
                    "error": "Address Not Found",
                    "description": "Modbus address does not map to any PLC register"
                }), 404
            
            return jsonify({
                "modbus_address": modbus_address,
                "plc_make": plc_make,
                "plc_type": plc_type,
                "results": results
            })

    except Exception as e:
        print(f"Error during reverse conversion: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": f"Conversion failed: {str(e)}"
        }), 500


@reverse_convert_blueprint.route("/api/batch-reverse-convert", methods=["POST"])
def batch_reverse_convert_api():
    """
    API endpoint for batch reverse conversion
    
    Request Body (JSON):
    {
        "plc_make": "Delta",
        "plc_model": "SV2",
        "addresses": [
            {"modbus": "2148", "type": "bit"},
            {"modbus": "4196", "type": "word"},
            {"modbus": "100"}  // type optional
        ]
    }
    
    Returns:
        JSON with array of conversion results
    """
    try:
        data = request.get_json()
        
        plc_make = data.get("plc_make", "Delta")
        plc_model = data.get("plc_model")
        addresses = data.get("addresses", [])
        
        if not plc_model or not addresses:
            return jsonify({
                "error": "Missing required fields: plc_model and addresses"
            }), 400
        
        results = []
        
        for addr_info in addresses:
            modbus_addr = addr_info.get("modbus")
            addr_type = addr_info.get("type")
            
            if not modbus_addr:
                results.append({
                    "error": "Missing modbus address",
                    "input": addr_info
                })
                continue
            
            # If type specified
            if addr_type:
                plc_addr, desc = Reverse_Convert.modbus_to_plc(
                    plc_make, plc_model, modbus_addr, addr_type
                )
                
                results.append({
                    "modbus_address": modbus_addr,
                    "plc_address": plc_addr,
                    "addr_type": addr_type,
                    "description": desc,
                    "success": not any(err in plc_addr for err in ["Unsupported", "Invalid", "Not Found"])
                })
            else:
                # Find all possible matches
                matches = Reverse_Convert.find_all_possible_plc_addresses(
                    plc_make, plc_model, modbus_addr
                )
                
                results.append({
                    "modbus_address": modbus_addr,
                    "matches": matches,
                    "success": len(matches) > 0
                })
        
        return jsonify({
            "plc_make": plc_make,
            "plc_model": plc_model,
            "results": results
        })
    
    except Exception as e:
        print(f"Error during batch reverse conversion: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": f"Batch conversion failed: {str(e)}"
        }), 500