# Forestry production processing

Processes FAOSTAT primary forestry production into a tidy long table
mirroring the shape of `crop_livestock_production`. Output rows are
`(ISO3, EXIOBASE product code, EXIOBASE sub-product, year)` with
quantities in m³.

## Data source

FAOSTAT Forestry Production and Trade domain (`FO`):
- Domain page: https://www.fao.org/faostat/en/#data/FO
- Bulk URL: `http://fenixservices.fao.org/faostat/static/bulkdownloads/Forestry_E_All_Data.zip`

The bulk URL pattern is stable (same as the other FAOSTAT bulks used
by this repo). Updated annually by FAO, typically December for the
previous calendar year.

## Item codes used

Two mutually-exclusive aggregates that together sum to total roundwood:

- `1865` Industrial roundwood → `plantation industrial`
- `1864` Wood fuel → `plantation fuelwood`

Together: `1864 + 1865 = 1861` (Roundwood total). Coniferous /
non-coniferous splits (`1862/1863`, `1866/1867`) exist in FAOSTAT but
are subsets of these and would double-count if included.

## Element filter

The FAOSTAT FO bulk publishes Production, Import, and Export rows for
every item, all sharing Item Code. The download handler
(`download/handlers.get_forestry`) filters to Element Code in
[5500, 5519] (the production series) before writing
`refreshed_forestry.csv`, so downstream code sees only one row per
(country, item).

## Output

`whole_forestry_calculation()` returns a DataFrame; `run_all.py`
writes `final_tables/forestry_final_runall.csv`.

## Validation

Global 2022 totals match FAO published series:

| | Module output | FAO published |
|---|---:|---:|
| Industrial roundwood | 2,049 Mm³ | ~2,030 Mm³ |
| Wood fuel            | 1,947 Mm³ | ~1,930 Mm³ |
| Total roundwood      | 3,996 Mm³ | ~3,966 Mm³ |

Top-10 industrial roundwood producers (USA, Russia, Brazil, China,
Canada, Indonesia, Sweden, Germany, Finland, India) match FAOSTAT
rankings.
