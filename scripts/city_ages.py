"""Victim ages for the city-file location check, from Dallas OpenData's Police Person table.

The city's incident file (Police Incidents, qv6i-rri7) has no victim age, and the kit's tract model needs it. The
Police Person table (chez-ydz4) lists each person in an incident with an age at the time of the offense. There is no
shared person key, so victims are linked by incident number, race, ethnicity and sex:

  - one person row in that cell: its age goes to every incident row in the cell (a victim of two offenses has two rows)
  - as many person rows as incident rows: the cell's ages are paired with its rows. Who got which age within the cell
    is arbitrary, but they are the ages of those victims, so counts by age band are exact
  - anything else: age stays missing (no imputation), and those victims drop out of the model only

Only the columns needed for the link are fetched (no names), for victims who are individuals, incident years 2021 on
(late reports of 2022 to 2025 assaults carry earlier or later incident years only rarely; the link rate says how many).

  python scripts/city_ages.py            ->  data/raw/dallas_person_victims.csv (+ .source.json),
                                             data/city/dallas_city_<kind>_aged.csv, out/city_ages.json
"""
import csv
import datetime as dt
import io
import json
import pathlib
import urllib.parse
import urllib.request

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://www.dallasopendata.com/resource/chez-ydz4.csv"
SELECT = "incidentnum,servyr,involvement,persontype,race,ethnic,sex,ageatoffensetime"
WHERE = "involvement = 'Victim' AND persontype = 'Individual' AND servyr >= 2021"
RAW = ROOT / "data/raw/dallas_person_victims.csv"
KINDS = ("simple", "aggravated")
KEY = ["incidentnum", "race", "ethnicity", "sex"]


def fetch(page=50000):
    rows, offset, header = [], 0, None
    while True:
        q = urllib.parse.urlencode({"$select": SELECT, "$where": WHERE, "$order": ":id", "$limit": page, "$offset": offset})
        req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": "disparity-kit"})
        r = list(csv.reader(io.StringIO(urllib.request.urlopen(req, timeout=300).read().decode("utf-8"))))
        header, body = r[0], r[1:]
        rows += body
        if len(body) < page:
            break
        offset += page
    with open(RAW, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(header); w.writerows(rows)
    side = {"url": "https://www.dallasopendata.com/d/chez-ydz4", "platform": "socrata", "api": API, "select": SELECT, "where": WHERE,
            "why": "only victims who are individuals, and only the columns needed to link ages (the table also holds names)",
            "fetched_at": dt.datetime.now().isoformat(timespec="seconds"), "rows": len(rows)}
    pathlib.Path(str(RAW) + ".source.json").write_text(json.dumps(side, indent=1))
    print(f"wrote {RAW} ({len(rows):,} rows)")


def main():
    if not RAW.exists():
        fetch()
    per = pd.read_csv(RAW, dtype=str, keep_default_na=False).rename(columns={"ethnic": "ethnicity"})
    per["age"] = pd.to_numeric(per["ageatoffensetime"], errors="coerce")
    per = per.sort_values(KEY + ["age"])
    stats = {}
    for kind in KINDS:
        src = ROOT / f"data/city/dallas_city_{kind}.csv"
        inc = pd.read_csv(src, dtype=str, keep_default_na=False)
        inc["race"], inc["ethnicity"], inc["sex"] = inc["comprace"], inc["compethnicity"], inc["compsex"]
        inc["_row"] = range(len(inc))
        n_inc = inc.groupby(KEY)["_row"].transform("size")
        p_cells = per.groupby(KEY)["age"].agg(list)
        inc["_ages"] = inc.set_index(KEY).index.map(p_cells)
        inc["_rank"] = inc.groupby(KEY)["_row"].rank(method="first").astype(int) - 1
        def pick(r, n):
            ages = r["_ages"]
            if not isinstance(ages, list):
                return None, "no person row"
            if len(ages) == 1:
                return ages[0], "one person"
            if len(ages) == n:
                return ages[r["_rank"]], "paired in cell"
            return None, "counts differ"
        out = [pick(r, n) for (_, r), n in zip(inc.iterrows(), n_inc)]
        inc["victim_age"] = [a for a, _ in out]
        inc["age_link"] = [s for _, s in out]
        dest = ROOT / f"data/city/dallas_city_{kind}_aged.csv"
        inc.drop(columns=["_row", "_ages", "_rank", "race", "ethnicity", "sex"]).to_csv(dest, index=False)
        win = inc[inc["date1"].str[:4].between("2022", "2025")]
        stats[kind] = {"rows_in_window": len(win), "link": win["age_link"].value_counts().to_dict(),
                       "age_known_pct": round(float(pd.to_numeric(win["victim_age"], errors="coerce").notna().mean() * 100), 1),
                       "age_known_pct_women": round(float(pd.to_numeric(win.loc[win["compsex"] == "Female", "victim_age"], errors="coerce").notna().mean() * 100), 1),
                       "under_17_linked": int((pd.to_numeric(win["victim_age"], errors="coerce") < 17).sum())}
        print(f"wrote {dest}: {stats[kind]}")
    (ROOT / "out" / "city_ages.json").write_text(json.dumps(stats, indent=1, default=int) + "\n")


if __name__ == "__main__":
    main()
