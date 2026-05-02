# -------------------------------------
#  Reverse Conversion: Modbus → PLC Address
# -------------------------------------

from Convert import PLC_MAPPINGS


def modbus_to_plc(plc_make: str, plc_model: str, modbus_address: str, addr_type: str) -> tuple[str, str]:
    """
    Convert Modbus address back to PLC address.
    
    Args:
        plc_make: Manufacturer name (e.g., "Delta")
        plc_model: Model name (e.g., "SV2", "ES2", "AS")
        modbus_address: Modbus address as string (raw or processed)
        addr_type: "bit" or "word"
    
    Returns:
        Tuple of (plc_address, description) as strings
        Example: ("D100", "Data register 100") or ("Error", "Invalid address")
    """
    
    # Validate PLC make and model
    if plc_make not in PLC_MAPPINGS:
        return ("Unsupported PLC Make", "Invalid manufacturer")
    
    if plc_model not in PLC_MAPPINGS[plc_make]:
        return ("Unsupported PLC Model", "Invalid model")
    
    model_mappings = PLC_MAPPINGS[plc_make][plc_model]
    
    # Parse modbus address (can be raw or processed)
    try:
        modbus_addr = int(modbus_address)
    except ValueError:
        return ("Invalid Modbus Address", "Must be a number")
    
    # Try to find matching register type and calculate PLC address
    if plc_model == "AS":
        return _reverse_convert_as_series(modbus_addr, addr_type, model_mappings)
    else:
        return _reverse_convert_standard_series(modbus_addr, addr_type, model_mappings)


def _reverse_convert_standard_series(modbus_addr: int, addr_type: str, model_mappings: dict) -> tuple[str, str]:
    """
    Reverse conversion for standard Delta PLC models.
    Handles both raw and processed Modbus addresses.
    """
    
    # Generate raw address candidates
    # User might provide:
    # 1. Raw address (e.g., 404197, 2149, 101025)
    # 2. Processed address (e.g., 4196, 2148, 1024)
    # 3. Processed with leading digit removed (e.g., 04196)
    
    raw_candidates = set()
    
    # Direct input
    raw_candidates.add(modbus_addr)
    raw_candidates.add(modbus_addr + 1)  # If user gave processed, add 1 to get raw
    
    # If looks like processed address (no leading 1 or 4), try adding prefixes
    if modbus_addr < 100000:
        for prefix in ['1', '4']:
            # Try as-is with prefix
            raw_candidates.add(int(prefix + str(modbus_addr)))
            # Try +1 with prefix
            raw_candidates.add(int(prefix + str(modbus_addr + 1)))
    
    for reg_type, type_mappings in model_mappings.items():
        if addr_type not in type_mappings:
            continue
        
        ranges = type_mappings[addr_type]
        
        for start_plc, end_plc, modbus_start in ranges:
            # Check all possible raw address candidates
            for raw_candidate in raw_candidates:
                if modbus_start <= raw_candidate <= modbus_start + (end_plc - start_plc):
                    offset = raw_candidate - modbus_start
                    plc_address = start_plc + offset
                    
                    # Format the PLC address
                    plc_addr_str = f"{reg_type}{int(plc_address)}"
                    
                    # Create description
                    type_desc = "bit" if addr_type == "bit" else "word"
                    desc = f"{reg_type} register {int(plc_address)} ({type_desc})"
                    
                    return (plc_addr_str, desc)
    
    return ("Address Not Found", "Modbus address does not map to any PLC register")


def _reverse_convert_as_series(modbus_addr: int, addr_type: str, model_mappings: dict) -> tuple[str, str]:
    """
    Reverse conversion for AS series (handles multi-char prefixes and bit addressing).
    """
    
    # Generate raw address candidates
    raw_candidates = set()
    
    # Direct input
    raw_candidates.add(modbus_addr)
    raw_candidates.add(modbus_addr + 1)
    
    # If looks like processed address, try adding prefixes
    if modbus_addr < 100000:
        for prefix in ['1', '3', '4']:
            raw_candidates.add(int(prefix + str(modbus_addr)))
            raw_candidates.add(int(prefix + str(modbus_addr + 1)))
    
    # Check each register type (sorted by length for multi-char prefixes)
    for reg_type in sorted(model_mappings.keys(), key=len, reverse=True):
        type_mappings = model_mappings.get(reg_type, {})
        
        if addr_type not in type_mappings:
            continue
        
        ranges = type_mappings[addr_type]
        
        for start_plc, end_plc, modbus_start in ranges:
            # Check all possible raw address candidates
            for raw_candidate in raw_candidates:
                # Calculate range
                if isinstance(start_plc, float):
                    # Bit addressing (e.g., X0.0 to X63.15)
                    max_modbus = modbus_start + int(end_plc) * 16 + 15
                    
                    if modbus_start <= raw_candidate <= max_modbus:
                        offset = raw_candidate - modbus_start
                        base = offset // 16
                        bit = offset % 16
                        
                        # Format as X0.0 style
                        plc_addr_str = f"{reg_type}{base}.{bit}"
                        desc = f"{reg_type} register {base} bit {bit}"
                        
                        return (plc_addr_str, desc)
                else:
                    # Standard word/bit addressing
                    max_modbus = modbus_start + (end_plc - start_plc)
                    
                    if modbus_start <= raw_candidate <= max_modbus:
                        offset = raw_candidate - modbus_start
                        plc_address = start_plc + offset
                        
                        plc_addr_str = f"{reg_type}{int(plc_address)}"
                        
                        type_desc = "bit" if addr_type == "bit" else "word"
                        desc = f"{reg_type} register {int(plc_address)} ({type_desc})"
                        
                        return (plc_addr_str, desc)
    
    return ("Address Not Found", "Modbus address does not map to any PLC register")


def find_all_possible_plc_addresses(plc_make: str, plc_model: str, modbus_address: str) -> list[dict]:
    """
    Find ALL possible PLC addresses for a given Modbus address.
    Useful when user doesn't specify bit/word type.
    
    Returns:
        List of dictionaries with keys: plc_address, addr_type, description
    """
    
    results = []
    
    # Try both bit and word
    for addr_type in ["bit", "word"]:
        plc_addr, desc = modbus_to_plc(plc_make, plc_model, modbus_address, addr_type)
        
        if not plc_addr.startswith("Unsupported") and not plc_addr.startswith("Invalid") and not plc_addr.startswith("Address Not Found"):
            results.append({
                "plc_address": plc_addr,
                "addr_type": addr_type,
                "description": desc
            })
    
    return results


# -------------------------------------
#  Backward Compatibility Wrappers
# -------------------------------------

def reverse_sv2(modbus_address: str, addr_type: str) -> tuple[str, str]:
    """Reverse conversion for SV2"""
    return modbus_to_plc("Delta", "SV2", modbus_address, addr_type)

def reverse_es2(modbus_address: str, addr_type: str) -> tuple[str, str]:
    """Reverse conversion for ES2"""
    return modbus_to_plc("Delta", "ES2", modbus_address, addr_type)

def reverse_ex2(modbus_address: str, addr_type: str) -> tuple[str, str]:
    """Reverse conversion for EX2"""
    return modbus_to_plc("Delta", "EX2", modbus_address, addr_type)

def reverse_ss2(modbus_address: str, addr_type: str) -> tuple[str, str]:
    """Reverse conversion for SS2"""
    return modbus_to_plc("Delta", "SS2", modbus_address, addr_type)

def reverse_se(modbus_address: str, addr_type: str) -> tuple[str, str]:
    """Reverse conversion for SE"""
    return modbus_to_plc("Delta", "SE", modbus_address, addr_type)

def reverse_sa2(modbus_address: str, addr_type: str) -> tuple[str, str]:
    """Reverse conversion for SA2"""
    return modbus_to_plc("Delta", "SA2", modbus_address, addr_type)

def reverse_sx2(modbus_address: str, addr_type: str) -> tuple[str, str]:
    """Reverse conversion for SX2"""
    return modbus_to_plc("Delta", "SX2", modbus_address, addr_type)

def reverse_as_series(modbus_address: str, addr_type: str) -> tuple[str, str]:
    """Reverse conversion for AS series"""
    return modbus_to_plc("Delta", "AS", modbus_address, addr_type)

