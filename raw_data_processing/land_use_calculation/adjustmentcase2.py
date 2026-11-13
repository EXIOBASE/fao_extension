"""Rescaling of a breakdown's parts to its total for the case-2 and case-4
countries (landuse.py, case2.py, case4.py).

In the years ``relevant_years_adjust2`` the parts are ``list3`` (minor1 and
minor2, plus minor3 when it is an exception item); in ``relevant_years_adjust``
all three. Each year goes through ``adjustment.adjust`` with that part list,
so the rule is the one of adjustment.py (every reported part multiplied by
total / sum(parts), the sum taken before any part changes; with
adjustment.RESCALE_ONLY_COMPLETE only where every listed part is reported).

Until 2026-11-14 this module divided by the running sum: after the first part
was rescaled the sum included its new value, so the next part got a different
factor and the parts did not add up to the total; a year whose total was
missing reused the previous year's parts. Same defect as adjustment.py before
4927a6a (R-AGR-02).
"""
import yaml

import adjustment


def adjust(landuse, dfs, code, years, diagram, key, country, relevant_years_adjust2,
           relevant_years_adjust, list2, list3):
    with open(r'aux_data/parameters.yaml') as file:
        parameters = yaml.load(file, Loader=yaml.FullLoader)
    if not diagram.get(key).get("minor3") in parameters.get("exeptions"):
        list3 = ['minor1', 'minor2']
    for year in relevant_years_adjust2:
        adjustment.adjust(landuse, dfs, code, year, diagram, key, country, parts=tuple(list3))
    for year in relevant_years_adjust:
        adjustment.adjust(landuse, dfs, code, year, diagram, key, country,
                          parts=adjustment.PARTS)
    return landuse
