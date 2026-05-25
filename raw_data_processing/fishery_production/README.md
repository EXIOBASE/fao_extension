# Fishery production processing

Processes FAO FishStat global production into a tidy long table mirroring the
shape of `crop_livestock_production`. Output rows are
`(ISO3, EXIOBASE product code, EXIOBASE sub-product, source_category, year)`
with quantities in tonnes.

## Data source: FAO direct bulk download

```
https://www.fao.org/fishery/static/Data/Aquaculture_<release>.zip
https://www.fao.org/fishery/static/Data/Capture_<release>.zip
```

This is the **authoritative FAO source** — the same data the FishStatJ
desktop tool consumes. The directory listing publishes annual release
zips with a stable naming pattern; the back catalogue goes to 2017
(`Aquaculture_2017.1.1.zip` through `Aquaculture_2026.1.0.zip` as of
this writing).

**Update workflow:** `run_all.py` asks `download.main` to discover the
newest matching Aquaculture/Capture release by default. To force a fresh
remote check and re-download, run `run_all.py --refresh-downloads`.
`fishstat_release` in `parameters.yaml` remains as a direct-module
fallback/documentation value.

The download handler caches under `<storage_path>/download/`, extracts
into `<storage_path>/data/fishstat/`, and the processing module reads
from there.

### Why not the FishStatJ desktop tool?

FishStatJ is the Java GUI; you'd have to install it and click through
exports. The bulk zips at the URL above contain the same CSVs,
without the desktop dependency.

### Why not the CRAN R package (`fishstat`)?

It's a community wrapper around exactly these FAO bulk zips,
maintained by Arni Magnusson at FAO/SOFIA-TAF. The package uses the
same upstream data, just repackaged as `.RData`. Direct from FAO:

- One less intermediary
- ~1-2 weeks faster to get a new release (CRAN has a publication lag)
- No `pyreadr` Python dependency

## Sub-product split below EXIOBASE p05

EXIOBASE has a single fishery product (`p05`). For downstream extensions
that need water- or land-intensity coefficients (notably the water
extension's aquaculture rows) we keep four sub-product categories,
mapped from the FAO ISSCAAP major groups:

- `inland fish`     — freshwater + diadromous finfish
- `marine fish`     — marine finfish
- `crustaceans`     — shrimps, crabs, lobsters
- `molluscs`        — oysters, mussels, scallops, cephalopods
- `other aquatic`   — plants, mammals, reptiles, miscellaneous

The runtime mapping is the `ISSCAAP_TO_SUBPRODUCT` dict in `fishery.py`;
the documented version is `aux_data/List_Primary_fishery_FAO-CPA-EXIOBASE.csv`.

## Source categories

The `source_category` column carries the freshwater-relevance flag:

- `aquaculture inland`   — inland freshwater aquaculture (relevant for blue water)
- `aquaculture brackish` — coastal/brackish aquaculture (small blue water)
- `aquaculture marine`   — marine aquaculture (~zero blue water)
- `capture inland`       — inland capture fisheries (rivers, lakes)
- `capture marine`       — marine capture fisheries

Aquaculture environment comes from the `ENVIRONMENT.ALPHA_2_CODE`
column in `Aquaculture_Quantity.csv` (IN/BW/MA). Capture inland-vs-
marine is derived by joining `AREA.CODE` to
`CL_FI_WATERAREA_GROUPS.csv > InlandMarine_Group_En`.

## Output

`whole_fishery_calculation()` returns a DataFrame; `run_all.py` writes
`final_tables/fishery_final_runall.csv`. Optionally append as a sheet
`Production_aquaculture` to `final/EXIOBASE_allocation_FAO_newMthod_*.xlsx`.

## Dependencies

`pandas`, `pyyaml` — already used by the rest of the repo. No `pyreadr`.
