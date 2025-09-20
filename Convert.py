# -------------------------------------
#  Master Mapping Dictionary
# -------------------------------------

PLC_MAPPINGS = {
    "Delta":{
        "SV2": {
            "S": {"bit" : [(0,255,1),(246,511,247),(512,767,513),(768,1023,769)] },
            "X": {"bit" : [(0,377,101025)] },
            "Y": {"bit" : [(0,377,1281)] },
            "T": {"bit" : [(0,255,1537)],
                  "word": [(0,255,401537)] },
            "M": {"bit" : [(0,255,2049),(256,511,2305),(512,767,2561),(768,1023,2817),
                        (1024,1279,3073),(1280,1535,3329),(1536,1791,45057),
                        (1792,2047,45313),(2048,2303,45569),(2304,2559,45825),
                        (2560,2815,46081),(2816,3071,46337),(3072,3327,46593),
                        (3328,3583,46849),(3584,3839,47105),(3840,4095,47361),
            ] },
            "D": {"word" : [(0,255,404097),(256,511,404353),(512,767,404609),(768,1023,404865),
                            (1024,1279,405121),(1280,1535,405377),(1536,1791,405633),
                            (1792,2047,405889),(2048,2303,406145),(2304,2559,406401),
                            (2560,2815,406657),(2816,3071,406913),(3072,3327,407169),
                            (3328,3583,407425),(3584,3839,407681),(3840,4095,407937),
                            (4096,4351,436865),(4352,4607,437121),(4608,4863,437377),
                            (4864,5119,437633),(5120,5375,437889),(5376,5631,438145),
                            (5632,5887,438401),(5888,6143,438657),(6144,6399,438913),
                            (6400,6655,439169),(6656,6911,439425),(6912,7167,439681),
                            (7168,7423,439937),(7424,7679,440193),(7680,7935,440449),
                            (7936,8191,440705),(8192,8447,440961),(8448,8703,441217),
                            (8704,8959,441473),(8960,9215,441729),(9216,9471,441985),
                            (9472,9727,442241),(9728,9983,442497),(9984,10239,442753),
                            (10240,10495,443009),(10496,10751,443247),(10752,11007,443503),
                            (11008,11263,443759),(11264,11519,444015),(11520,11775,444271),
                            (11776,11999,444527),
            ] }
        },
        "ES2": {
            "S": {"bit" : [(0,255,1),(256,511,257),(512,767,513),(768,1023,769)] },
            "X": {"bit" : [(0,377,101025)] },
            "Y": {"bit" : [(0,377,1281)] },
            "T": {"bit" : [(0,255,1537)],
                  "word": [(0,255,401537)] },
            "M": {"bit" : [(0,1535,2049),(1536,4095,45057)] },
            "D": {"word": [(0,1279,404097),
                            (1280,4095,405377),
                            (4096,8191,436865),
                            (8192,9999,440961)]}
        },
        "EX2": {
            "S": {"bit" : [(0,255,1),(256,511,257),(512,767,513),(768,1023,769)] },
            "X": {"bit" : [(0,377,101025)] },
            "Y": {"bit" : [(0,377,1281)] },
            "T": {"bit" : [(0,255,1537)],
                  "word": [(0,255,401537)] },
            "M": {"bit" : [(0,1535,2049),(1536,4095,45057)] },
            "D": {"word": [(0,1279,404097),
                            (1280,4095,405377),
                            (4096,8191,436865),
                            (8192,9999,440961)]}
        },
         "SS2": {
            "S": {"bit" : [(0,255,1),(256,511,257),(512,767,513),(768,1023,769)] },
            "X": {"bit" : [(0,377,101025)] },
            "Y": {"bit" : [(0,377,1281)] },
            "T": {"bit" : [(0,255,1537)],
                  "word": [(0,255,401537)] },
            "M": {"bit" : [(0,1535,2049),(1536,4095,45057)] },
            "D": {"word": [(0,1279,404097),
                           (1280,4095,405377),
                           (4096,5119,436865)]}
        },
        "SE": {
            "S": {"bit" : [(0,255,1),(256,511,257),(512,767,513),(768,1023,769)] },
            "X": {"bit" : [(0,377,101025)] },
            "Y": {"bit" : [(0,377,1281)] },
            "T": {"bit" : [(0,255,1537)],
                  "word": [(0,255,401537)] },
            "M": {"bit" : [(0,1535,2049),(1536,4095,45057)] },
            "D": {"word": [(0,1279,404097),
                            (1280,4095,405377),
                            (4096,8191,436865),
                            (8192,9999,440961),
                            (10000,11999,442769)]}
        },
        "SA2": {
            "S": {"bit" : [(0,255,1),(256,511,257),(512,767,513),(768,1023,769)] },
            "X": {"bit" : [(0,377,101025)] },
            "Y": {"bit" : [(0,377,1281)] },
            "T": {"bit" : [(0,255,1537)],
                  "word": [(0,255,401537)] },
            "M": {"bit" : [(0,1535,2049),(1536,4095,45057)] },
            "D": {"word": [(0,1279,404097),
                           (1280,4095,405377),
                           (4096,8191,436865),
                           (8192,9999,440961)] }
        },
        "SX2": {
            "S": {"bit" : [(0,255,1),(256,511,257),(512,767,513),(768,1023,769)] },
            "X": {"bit" : [(0,377,101025)] },
            "Y": {"bit" : [(0,377,1281)] },
            "T": {"bit" : [(0,255,1537)],
                  "word": [(0,255,401537)] },
            "M": {"bit" : [(0,1535,2049),(1536,4095,45057)] },
            "D": {"word": [(0,1279,404097),
                           (1280,4095,405377),
                           (4096,8191,436865),
                           (8192,9999,440961)]}
        },
        "AS": {
            "X" : {"bit"  : [(0.0, 63.15, 124577)],
                   "word"  : [(0,63,332769)] },
            "Y" : {"bit"  : [(0.0, 63.15, 40961)],
                   "word" : [(0, 63, 440961)] },
            "M" : {"bit"  : [(0, 8191, 1)]  },
            "SM": {"bit"  : [(0, 4095, 16385)] },
            "SR": {"word" : [(0, 2047, 449153)] },
            "D" : {"word" : [(0, 29999, 400001)]},
            "S" : {"bit"  : [(0, 2047, 20481)] },
            "T" : {"bit"  : [(0, 511, 57345)],
                   "word" : [(0, 511, 457345)] },
            "C" : {"bit"  : [(0, 511, 61441)], 
                   "word" : [(0, 511, 461441)] },
            "HC": {"bit"  : [(0, 255, 64513)], 
                   "word" : [(0, 255, 464513)] },
            "E" : {"word" : [(0, 9, 465025)]}
        }
    }
}


def sv2(plc_address: str, addr_type: str) -> tuple[str, str]:
    global PLC_MAPPINGS
    
    reg_type = plc_address[0].upper()
    try:
        reg_address = int(plc_address[1:])
    except ValueError:
        return ("Invalid Address", "Invalid Address")
    
    maps = PLC_MAPPINGS["Delta"]["SV2"].get(reg_type, {}).get(addr_type, {})
    if not maps:
        return ("Unsupported Register Type", "Unsupported Register Type")

    raw_address = None
    for start, end, modbus_start in maps:
        if start <= reg_address <= end:
            raw_address = modbus_start + (reg_address - start)
            break

    if raw_address is None:
        return ("Unsupported Address Range", "Unsupported Address Range")

    # Processing rules for specific register types
    if reg_type == "D" or addr_type == "word":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("4") else raw_address - 1
    elif reg_type == "X":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("1") else raw_address - 1
    elif reg_type in {"M", "S", "T", "Y"}:
        processed_address = raw_address - 1
    else:
        processed_address = raw_address

    return str(raw_address), str(processed_address)



def es2(plc_address: str, addr_type: str) -> tuple[str, str]:
    global PLC_MAPPINGS
    
    reg_type = plc_address[0].upper()
    try:
        reg_address = int(plc_address[1:])
    except ValueError:
        return ("Invalid Address", "Invalid Address")
    
    maps = PLC_MAPPINGS["Delta"]["ES2"].get(reg_type, {}).get(addr_type, {})
    if not maps:
        return ("Unsupported Register Type", "Unsupported Register Type")

    raw_address = None
    for start, end, modbus_start in maps:
        if start <= reg_address <= end:
            raw_address = modbus_start + (reg_address - start)
            break

    if raw_address is None:
        return ("Unsupported Address Range", "Unsupported Address Range")

    # Processing rules for specific register types
    if reg_type == "D" or addr_type == "word":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("4") else raw_address - 1
    elif reg_type == "X":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("1") else raw_address - 1
    elif reg_type in {"M", "S", "T", "Y"}:
        processed_address = raw_address - 1
    else:
        processed_address = raw_address

    return str(raw_address), str(processed_address)



def ex2(plc_address: str, addr_type: str) -> tuple[str, str]:
    global PLC_MAPPINGS
    
    reg_type = plc_address[0].upper()
    try:
        reg_address = int(plc_address[1:])
    except ValueError:
        return ("Invalid Address", "Invalid Address")
    
    maps = PLC_MAPPINGS["Delta"]["EX2"].get(reg_type, {}).get(addr_type, {})
    if not maps:
        return ("Unsupported Register Type", "Unsupported Register Type")

    raw_address = None
    for start, end, modbus_start in maps:
        if start <= reg_address <= end:
            raw_address = modbus_start + (reg_address - start)
            break

    if raw_address is None:
        return ("Unsupported Address Range", "Unsupported Address Range")

    # Processing rules for specific register types
    if reg_type == "D" or addr_type == "word":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("4") else raw_address - 1
    elif reg_type == "X":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("1") else raw_address - 1
    elif reg_type in {"M", "S", "T", "Y"}:
        processed_address = raw_address - 1
    else:
        processed_address = raw_address

    return str(raw_address), str(processed_address)



def ss2(plc_address: str, addr_type: str) -> tuple[str, str]:
    global PLC_MAPPINGS
    
    reg_type = plc_address[0].upper()
    try:
        reg_address = int(plc_address[1:])
    except ValueError:
        return ("Invalid Address", "Invalid Address")
    
    maps = PLC_MAPPINGS["Delta"]["SS2"].get(reg_type, {}).get(addr_type, {})
    if not maps:
        return ("Unsupported Register Type", "Unsupported Register Type")

    raw_address = None
    for start, end, modbus_start in maps:
        if start <= reg_address <= end:
            raw_address = modbus_start + (reg_address - start)
            break

    if raw_address is None:
        return ("Unsupported Address Range", "Unsupported Address Range")

    # Processing rules for specific register types
    if reg_type == "D" or addr_type == "word":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("4") else raw_address - 1
    elif reg_type == "X":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("1") else raw_address - 1
    elif reg_type in {"M", "S", "T", "Y"}:
        processed_address = raw_address - 1
    else:
        processed_address = raw_address

    return str(raw_address), str(processed_address)



def se(plc_address: str, addr_type: str) -> tuple[str, str]:
    global PLC_MAPPINGS
    
    reg_type = plc_address[0].upper()
    try:
        reg_address = int(plc_address[1:])
    except ValueError:
        return ("Invalid Address", "Invalid Address")
    
    maps = PLC_MAPPINGS["Delta"]["SE"].get(reg_type, {}).get(addr_type, {})
    if not maps:
        return ("Unsupported Register Type", "Unsupported Register Type")

    raw_address = None
    for start, end, modbus_start in maps:
        if start <= reg_address <= end:
            raw_address = modbus_start + (reg_address - start)
            break

    if raw_address is None:
        return ("Unsupported Address Range", "Unsupported Address Range")

    # Processing rules for specific register types
    if reg_type == "D" or addr_type == "word":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("4") else raw_address - 1
    elif reg_type == "X":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("1") else raw_address - 1
    elif reg_type in {"M", "S", "T", "Y"}:
        processed_address = raw_address - 1
    else:
        processed_address = raw_address

    return str(raw_address), str(processed_address)



def sa2(plc_address: str, addr_type: str) -> tuple[str, str]:
    global PLC_MAPPINGS
    
    reg_type = plc_address[0].upper()
    try:
        reg_address = int(plc_address[1:])
    except ValueError:
        return ("Invalid Address", "Invalid Address")
    
    maps = PLC_MAPPINGS["Delta"]["SA2"].get(reg_type, {}).get(addr_type, {})
    if not maps:
        return ("Unsupported Register Type", "Unsupported Register Type")

    raw_address = None
    for start, end, modbus_start in maps:
        if start <= reg_address <= end:
            raw_address = modbus_start + (reg_address - start)
            break

    if raw_address is None:
        return ("Unsupported Address Range", "Unsupported Address Range")

    # Processing rules for specific register types
    if reg_type == "D" or addr_type == "word":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("4") else raw_address - 1
    elif reg_type == "X":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("1") else raw_address - 1
    elif reg_type in {"M", "S", "T", "Y"}:
        processed_address = raw_address - 1
    else:
        processed_address = raw_address

    return str(raw_address), str(processed_address)



def sx2(plc_address: str, addr_type: str) -> tuple[str, str]:
    global PLC_MAPPINGS
    
    reg_type = plc_address[0].upper()
    try:
        reg_address = int(plc_address[1:])
    except ValueError:
        return ("Invalid Address", "Invalid Address")
    
    maps = PLC_MAPPINGS["Delta"]["SX2"].get(reg_type, {}).get(addr_type, {})
    if not maps:
        return ("Unsupported Register Type", "Unsupported Register Type")

    raw_address = None
    for start, end, modbus_start in maps:
        if start <= reg_address <= end:
            raw_address = modbus_start + (reg_address - start)
            break

    if raw_address is None:
        return ("Unsupported Address Range", "Unsupported Address Range")

    # Processing rules for specific register types
    if reg_type == "D" or addr_type == "word":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("4") else raw_address - 1
    elif reg_type == "X":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("1") else raw_address - 1
    elif reg_type in {"M", "S", "T", "Y"}:
        processed_address = raw_address - 1
    else:
        processed_address = raw_address

    return str(raw_address), str(processed_address)



def as_series(plc_address: str, addr_type: str) -> tuple[str, str]:
    global PLC_MAPPINGS
    
    # --- Find the correct register type (supports multi-char like SM, SR, HC) ---
    possible_types = sorted(PLC_MAPPINGS["Delta"]["AS"].keys(), key=len, reverse=True)
    reg_type = next((t for t in possible_types if plc_address.upper().startswith(t)), None)
    if not reg_type:
        return ("Unsupported Register Type", "Unsupported Register Type")

    # Extract the numeric/bit portion after the register prefix
    try:
        suffix = plc_address[len(reg_type):]
        reg_address = float(suffix) if "." in suffix else int(suffix)
    except ValueError:
        return ("Invalid Address", "Invalid Address")
    
    maps = PLC_MAPPINGS["Delta"]["AS"].get(reg_type, {}).get(addr_type, {})
    if not maps:
        return ("Unsupported Register Type", "Unsupported Register Type")

    raw_address = None
    for start, end, modbus_start in maps:
        if start <= reg_address <= end:
            if isinstance(reg_address, float):
                base = int(reg_address)
                bit = int(round((reg_address - base) * 100))  # handles .0–.15
                raw_address = modbus_start + base * 16 + bit
            else:
                raw_address = modbus_start + (reg_address - start)
            break

    if raw_address is None:
        return ("Unsupported Address Range", "Unsupported Address Range")

    # Processing rules
    if reg_type == "D" or addr_type == "word":
        processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("4") else raw_address - 1
    elif reg_type in {"X"}:
        if addr_type == "bit":
            processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("1") else raw_address - 1
        elif addr_type == "word":
            processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("3") else raw_address - 1
        else:
            processed_address = raw_address - 1
    
    elif reg_type in {"Y"}:
        if addr_type == "bit":
            processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("1") else raw_address - 1
        elif addr_type == "word":
            processed_address = int(str(raw_address)[1:]) - 1 if str(raw_address).startswith("4") else raw_address - 1
        else:
            processed_address = raw_address - 1

    elif reg_type in {"M", "S", "T", "SM", "SR", "HC"}:
        processed_address = raw_address - 1
    else:
        processed_address = raw_address

    return str(raw_address), str(processed_address)
