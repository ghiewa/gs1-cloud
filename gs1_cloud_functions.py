def get_gs1_mo(gtin):
    # Get the GS1 Member organisation based on the prefix of the GTIN

    import gs1_prefixes as pf

    gs1_mo = ""

    if gtin[0:6] == '000000':
        # GTIN-8
        if gtin[6:9] in pf.prefix:
            gs1_mo = pf.prefix[gtin[6:9]]
    elif gtin[1:6] in ('00001', '00002', '00003', '00004', '00005', '00006', '00007', '00008', '00009'):
        # GS1 US 00001 – 00009
        if gtin[1:6] in pf.prefix:
            gs1_mo = pf.prefix[gtin[1:6]]
    elif gtin[1:5] in ('0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009'):
        # GS1 US 0001 – 0009
        if gtin[1:5] in pf.prefix:
            gs1_mo = pf.prefix[gtin[1:5]]
    elif gtin[1:4] in pf.prefix:
        # All other prefixes
        # Exclude Global Office GTIN-8 range when used as GTIN-14
        if gtin[1:4] not in ('960', '961', '962', '963', '964', '965', '966', '967', '968', '969'):
            gs1_mo = pf.prefix[gtin[1:4]]

    return gs1_mo
