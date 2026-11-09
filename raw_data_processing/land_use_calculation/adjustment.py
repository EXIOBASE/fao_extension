PARTS = ('minor1', 'minor2', 'minor3')


def adjust(landuse, dfs, code, years, diagram, key, country):
    """Rescale the reported parts of breakdown `key` to its reported total.

    For country `code` and year column `years`, every part of `key` listed in
    `diagram` that the country has a nonzero value for is multiplied by
    value_major / sum(parts), the sum taken before any part is changed, so
    the parts add up to the total afterwards. Parts that are missing or zero
    stay as they are. Nothing changes when the total is missing or the parts
    sum to zero. `landuse` is changed in place and returned; `dfs` and
    `country` are unused and kept for the callers in landuse.py.

    Until 2026-11-10 the rescaling ran after the loop over the parts on the
    last loop value only: in a three-part breakdown only the third part was
    scaled (and the parts did not then sum to the total), in a two-part
    breakdown nothing was scaled.
    """
    rows = landuse['ISO3'] == code
    value_major = landuse.loc[rows & (landuse['Item Code'] == key), years]
    if value_major.isnull().all():
        return landuse
    value_major = float(value_major.dropna().iloc[0])

    country_items = set(landuse.loc[rows, 'Item Code'])
    minor_value = {}
    for part in PARTS:
        item = diagram.get(key).get(part)
        if item is None or item not in country_items:
            continue
        value = landuse.loc[rows & (landuse['Item Code'] == item), years]
        minor_value[item] = 0.0 if value.isnull().all() else float(value.dropna().iloc[0])

    total = sum(minor_value.values())
    if total == 0:
        return landuse

    factor = value_major / total
    for item, value in minor_value.items():
        if value != 0:
            landuse.loc[rows & (landuse['Item Code'] == item), years] = value * factor

    return landuse
