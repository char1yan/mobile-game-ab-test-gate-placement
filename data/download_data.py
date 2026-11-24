"""Download the raw dataset into data/raw/ (run from the repo root: python data/download_data.py)."""
from pathlib import Path
from urllib.request import urlretrieve

FILES = {
    # Cookie Cats A/B test data (DataCamp project, originally from Tactile Entertainment)
    "cookie_cats.csv": "https://raw.githubusercontent.com/robguilarr/ab_testing_cookie_cats/main/datasets/cookie_cats.csv",
}

raw = Path(__file__).parent / "raw"
raw.mkdir(exist_ok=True)
for name, url in FILES.items():
    print(f"Downloading {name} ...")
    urlretrieve(url, raw / name)
print("Done.")
