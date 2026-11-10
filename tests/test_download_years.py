"""One year window for every download task (download/main.py).

Step 1 kept crops and value of production to 2024 while steps 3 and 4 stop
at the year_of_interest end of aux_data/parameters.yaml, so step 3 failed
with KeyError 'Y2024'.

    .venv/Scripts/python.exe -m unittest discover -s tests
"""

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "download"))
import main  # noqa: E402


class DownloadYearsTest(unittest.TestCase):
    def test_configured_years_is_the_parameters_window(self):
        with open(REPO / "aux_data" / "parameters.yaml") as f:
            window = yaml.safe_load(f)["year_of_interest"]
        years = main.configured_years()
        self.assertEqual(years.start, window["begin"])
        self.assertEqual(years.stop - 1, window["end"])

    def test_every_task_gets_the_same_years(self):
        seen = {}

        def recorder(name):
            def run(relevant_years, download_path, data_path, **para):
                seen[name] = list(relevant_years)
            return run

        saved = {k: v["processor"] for k, v in main.DOWNLOAD_TASKS.items()}
        try:
            for k in main.DOWNLOAD_TASKS:
                main.DOWNLOAD_TASKS[k]["processor"] = recorder(k)
            with tempfile.TemporaryDirectory() as tmp:
                main.get_all(years=range(1961, 2024), storage_path=Path(tmp))
        finally:
            for k, p in saved.items():
                main.DOWNLOAD_TASKS[k]["processor"] = p
        self.assertEqual(set(seen), set(main.DOWNLOAD_TASKS))
        for name, years in seen.items():
            self.assertEqual(years, list(range(1961, 2024)), name)


if __name__ == "__main__":
    unittest.main()
