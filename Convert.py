# -------------------------------------
#  Master Mapping Dictionary
# -------------------------------------

PLC_MAPPINGS = {
    "SV2": {
        "S": [(0,255,1),(246,511,247),(512,767,513),(768,1023,769)],
        "X": [(0,377,101025)],
        "Y": [(0,377,1281)],
        "T": [(0,255,1537)],
        "C": [(0,199,3585),(200,255,3785)],
        "M": [
            (0,255,2049),(256,511,2305),(512,767,2561),(768,1023,2817),
            (1024,1279,3073),(1280,1535,3329),(1536,1791,45057),
            (1792,2047,45313),(2048,2303,45569),(2304,2559,45825),
            (2560,2815,46081),(2816,3071,46337),(3072,3327,46593),
            (3328,3583,46849),(3584,3839,47105),(3840,4095,47361),
        ],
        "D": [
            (0,255,404097),(256,511,404353),(512,767,404609),(768,1023,404865),
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
        ]
    }
}

# # alias mapping
# PLC_MAPPINGS["SV"]  = PLC_MAPPINGS["SV2"]
# PLC_MAPPINGS["SA2"] = PLC_MAPPINGS["ES2"]
# PLC_MAPPINGS["SS2"] = PLC_MAPPINGS["ES2"]
# PLC_MAPPINGS["SX2"] = PLC_MAPPINGS["ES2"]
# PLC_MAPPINGS["SE"]  = PLC_MAPPINGS["ES2"]


def sv2(plc_address: str) -> tuple:
    global PLC_MAPPINGS
    maps = PLC_MAPPINGS["SV2"]
    reg_type = plc_address[:1].upper()
    reg_address = int(plc_address[1:])
    raw_address = None
    processed_address = None

    for start, end, modbus_start in maps[reg_type]:
        if reg_address >= start and reg_address <= end:
            dif = reg_address - start
            raw_address = modbus_start + dif
            break
    
    if raw_address == None:
        return ("Unsupported Address","Unsupported Address")
    
    if reg_type == "D":
        value = raw_address if str(raw_address)[:1] != '4' else int(str(raw_address)[1:])
        processed_address = value - 1
    elif reg_type == "X":
        value = raw_address if str(raw_address)[:1] != '1' else int(str(raw_address)[1:])
        processed_address = value - 1
    elif reg_type == "M" or reg_type == "S" or reg_type == "T" or reg_type == "Y":
        processed_address = raw_address - 1
    else:
        processed_address = raw_address
    return (str(raw_address),str(processed_address))

