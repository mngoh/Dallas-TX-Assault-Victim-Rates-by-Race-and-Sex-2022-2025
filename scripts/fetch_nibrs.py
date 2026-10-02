"""Download the FBI's NIBRS incident files for Texas, one zip per year, as received.

The Crime Data Explorer (Documents & Downloads, "Download NIBRS data by state and year") serves each file through a
signed link from /LATEST/s3/signedurl?key=nibrs/incident/<year>/TX-<year>.zip. Each zip is saved to
data/raw/TX-<year>.zip with TX-<year>.zip.source.json beside it (key, time, size, sha256).

  python scripts/fetch_nibrs.py 2022 2023 2024 2025
"""
import datetime as dt
import hashlib
import json
import pathlib
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CDE = "https://cde.ucr.cjis.gov/LATEST/s3/signedurl"
UA = {"User-Agent": "disparity-kit"}


def get(url, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)


def main():
    for year in sys.argv[1:] or ["2022", "2023", "2024", "2025"]:
        key = f"nibrs/incident/{year}/TX-{year}.zip"
        signed = json.load(get(f"{CDE}?{urllib.parse.urlencode({'key': key})}")).get(key)
        if not signed:
            print(f"{year}: no file at {key}")
            continue
        dest = ROOT / f"data/raw/TX-{year}.zip"
        h = hashlib.sha256()
        with get(signed, timeout=1800) as r, open(dest, "wb") as fh:
            while chunk := r.read(1 << 20):
                h.update(chunk)
                fh.write(chunk)
        side = {"url": "https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads", "platform": "fbi-cde", "api": f"{CDE}?key={key}", "key": key,
                "fetched_at": dt.datetime.now().isoformat(timespec="seconds"), "bytes": dest.stat().st_size, "sha256": h.hexdigest(),
                "note": "FBI Crime Data Explorer, NIBRS incident data by state and year, Texas, as received"}
        pathlib.Path(str(dest) + ".source.json").write_text(json.dumps(side, indent=1))
        print(f"wrote {dest} ({dest.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
