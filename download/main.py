from pathlib import Path
from typing import Iterable, List, Optional, Union
from copy import deepcopy
import logging
import re

import requests

try:
    from . import handlers
except ImportError:  # pragma: no cover - keeps direct script execution working
    import handlers



FISHSTAT_BASE_URL = "https://www.fao.org/fishery/static/Data/"
FISHSTAT_FALLBACK_RELEASE = "2026.1.0"
FISHSTAT_RELEASE_PATTERN = re.compile(
    r"(Aquaculture|Capture)_(\d{4}\.\d+\.\d+)\.zip"
)


def _fishstat_release_key(release: str) -> tuple[int, ...]:
    return tuple(int(part) for part in release.split("."))


def discover_latest_fishstat_release() -> str:
    """Return the newest FishStat release available for both required zips."""
    response = requests.get(FISHSTAT_BASE_URL, timeout=30)
    response.raise_for_status()

    releases = {"Aquaculture": set(), "Capture": set()}
    for kind, release in FISHSTAT_RELEASE_PATTERN.findall(response.text):
        releases[kind].add(release)

    common_releases = releases["Aquaculture"] & releases["Capture"]
    if not common_releases:
        raise RuntimeError(
            "Could not find a FishStat release with both Aquaculture and Capture zips"
        )
    return max(common_releases, key=_fishstat_release_key)


def _fishstat_url(kind: str, release: str) -> str:
    return f"{FISHSTAT_BASE_URL}{kind}_{release}.zip"


def _apply_fishstat_release(tasks: dict, fishstat_release: str) -> Optional[str]:
    fishery_tasks = {"fishery_aquaculture", "fishery_capture"} & set(tasks)
    if not fishery_tasks:
        return None

    if fishstat_release.strip().lower() in {"latest", "auto"}:
        try:
            release = discover_latest_fishstat_release()
        except Exception as exc:  # noqa: BLE001
            release = FISHSTAT_FALLBACK_RELEASE
            logging.warning(
                "Could not discover latest FishStat release (%s). "
                "Falling back to %s.",
                exc,
                release,
            )
    else:
        release = fishstat_release

    if "fishery_aquaculture" in tasks:
        tasks["fishery_aquaculture"]["para"]["src_url"] = _fishstat_url(
            "Aquaculture", release
        )
    if "fishery_capture" in tasks:
        tasks["fishery_capture"]["para"]["src_url"] = _fishstat_url(
            "Capture", release
        )
    return release


DOWNLOAD_TASKS = dict(
    landuse=dict(
        para=dict(
            src_url="http://fenixservices.fao.org/faostat/static/bulkdownloads/Inputs_LandUse_E_All_Data.zip",
            csv_name=Path("Inputs_LandUse_E_All_Data_NOFLAG.csv"),
        ),
        processor=handlers.get_landuse,
    ),
    
    landcover=dict(
        para=dict(
            src_url="https://bulks-faostat.fao.org/production/Environment_LandCover_E_All_Data.zip",
            csv_name=Path("Environment_LandCover_E_All_Data_NOFLAG.csv"),
        ),
        processor=handlers.get_landcover,
    ),
    
    crop_livestock=dict(
        para=dict(
            src_url = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Production_Crops_Livestock_E_All_Data.zip",
            csv_name = Path("Production_Crops_Livestock_E_All_Data_NOFLAG.csv"),
        ),
        processor=handlers.get_crop_livestock,
    )    ,
    
    value_production=dict(
        para=dict(
            src_url = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Value_of_Production_E_All_Data.zip",
            csv_name = Path("Value_of_Production_E_All_Data.csv"),
        ),
        processor=handlers.get_value_production,
    ),

    # FAOSTAT Forestry Production and Trade (domain FO).
    # Annual update from FAO; URL pattern is stable across editions.
    forestry=dict(
        para=dict(
            src_url="http://fenixservices.fao.org/faostat/static/bulkdownloads/Forestry_E_All_Data.zip",
            csv_name=Path("Forestry_E_All_Data_NOFLAG.csv"),
        ),
        processor=handlers.get_forestry,
    ),

    # FishStat global production via FAO bulk downloads. get_all() resolves
    # the newest matching Aquaculture/Capture release unless a release is
    # provided explicitly.
    fishery_aquaculture=dict(
        para=dict(
            src_url="https://www.fao.org/fishery/static/Data/Aquaculture_2026.1.0.zip",
            csv_name=Path("fishstat/Aquaculture_Quantity.csv"),
        ),
        processor=handlers.get_fishery_aquaculture,
    ),
    fishery_capture=dict(
        para=dict(
            src_url="https://www.fao.org/fishery/static/Data/Capture_2026.1.0.zip",
            csv_name=Path("fishstat/Capture_Quantity.csv"),
        ),
        processor=handlers.get_fishery_capture,
    ),

)


def get_all(
    years: Optional[List[int]],
    storage_path: Path,
    tasks: Optional[Iterable[str]] = None,
    force_download: bool = False,
    fishstat_release: str = "latest",
):
    """Download and process all FAO data

    Parameter
    ---------
    years: list[int],
        all years to process

    storage_path: pathlib.Path
        Location for storing the data

    tasks: iterable[str], optional
        Names from DOWNLOAD_TASKS to run. If omitted, all tasks are run.

    force_download: bool, optional
        Download source archives even if a local zip with the same name exists.

    fishstat_release: str, optional
        FishStat release to use, or "latest" to discover it from FAO.

    """
    download_path = Path(storage_path / "download")
    download_path.mkdir(exist_ok=True, parents=True)
    data_path = Path(storage_path / "data")
    data_path.mkdir(exist_ok=True, parents=True)

    if tasks is None:
        selected_tasks = deepcopy(DOWNLOAD_TASKS)
    else:
        tasks = list(tasks)
        unknown_tasks = sorted(set(tasks) - set(DOWNLOAD_TASKS))
        if unknown_tasks:
            raise KeyError(f"Unknown download task(s): {', '.join(unknown_tasks)}")
        selected_tasks = {
            taskname: deepcopy(DOWNLOAD_TASKS[taskname]) for taskname in tasks
        }

    fishstat_release_used = _apply_fishstat_release(
        selected_tasks, fishstat_release=fishstat_release
    )

    for taskname, task in selected_tasks.items():
        

        logging.info(f"Processing {taskname}")
        task["processor"](
            relevant_years=years,
            download_path=download_path,
            data_path=data_path,
            force_download=force_download,
            **task["para"]
        )

    return {"fishstat_release": fishstat_release_used}
        



