PARTS = ('minor1', 'minor2', 'minor3')

# R-AGR-02 / DEC-56 (2026-11-14), held. As written in 4927a6a the reported parts
# of a breakdown take the whole total even where a part is not reported (Saudi
# Arabia's cultivated pasture 826 to 1,700,000 km2 with no naturally growing
# pasture reported). With RESCALE_ONLY_COMPLETE the parts are rescaled only
# when every part the diagram lists is reported for the country and year (a
# reported zero counts as reported); a breakdown with a part missing is left as
# it is. On since 2026-11-20 (DEC-56 decided: the variant that keeps values
# sane); False gives 4927a6a as written. README "Rescaling of the parts" has
# both measured.
RESCALE_ONLY_COMPLETE = True


def adjust(landuse, dfs, code, years, diagram, key, country, parts=PARTS):
    """Rescale the reported parts of breakdown `key` to its reported total.

    For country `code` and year column `years`, every part of `key` listed in
    `diagram` that the country has a nonzero value for is multiplied by
    value_major / sum(parts), the sum taken before any part is changed, so
    the parts add up to the total afterwards. Parts that are missing or zero
    stay as they are. Nothing changes when the total is missing or the parts
    sum to zero. `landuse` is changed in place and returned; `dfs` and
    `country` are unused and kept for the callers in landuse.py. `parts`: the
    diagram keys of the parts (adjustmentcase2 passes a shorter list). With
    RESCALE_ONLY_COMPLETE a breakdown with a listed part missing or empty for
    the country and year is left as it is.

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
    for part in parts:
        item = diagram.get(key).get(part)
        if item is None:
            continue
        if item not in country_items:
            if RESCALE_ONLY_COMPLETE:
                return landuse
            continue
        value = landuse.loc[rows & (landuse['Item Code'] == item), years]
        if value.isnull().all():
            if RESCALE_ONLY_COMPLETE:
                return landuse
            minor_value[item] = 0.0
        else:
            minor_value[item] = float(value.dropna().iloc[0])

    total = sum(minor_value.values())
    if total == 0:
        return landuse

    factor = value_major / total
    for item, value in minor_value.items():
        if value != 0:
            landuse.loc[rows & (landuse['Item Code'] == item), years] = value * factor

    return landuse
