"""Two working copies of the raw data, so the audits and the city-file steps read small files.

  data/interim/victim_offenses_dpd.csv     the flattened NIBRS file, Dallas Police Department rows only (for the audit;
                                           the full file keeps the other agencies for the exclusion counts)
  data/interim/dallas_incidents_slim.csv   the city's Police Incidents file (1.5 GB) cut to the columns used here, with
                                           latitude and longitude parsed from its location column

  python scripts/slim_inputs.py
"""
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CITY_COLS = ["incidentnum", "servnumid", "offincident", "premise", "beat", "division", "sector", "district", "date1", "time1", "year1",
             "reporteddate", "involvement", "victimtype", "comprace", "compethnicity", "compsex", "family", "weaponused", "offensecode",
             "penalcode", "ucr_offense", "nibrs_crime", "nibrs_crime_category", "nibrs_crimeagainst", "nibrs_code", "x_coordinate",
             "y_cordinate", "zip_code", "city", "geocoded_column"]


def main():
    v = pd.read_csv(ROOT / "data/interim/victim_offenses.csv", low_memory=False, dtype=str)
    v[v["ori"] == "TXDPD0000"].to_csv(ROOT / "data/interim/victim_offenses_dpd.csv", index=False)
    d = pd.read_csv(ROOT / "data/raw/dallas_incidents.csv", usecols=CITY_COLS, dtype=str, keep_default_na=False, low_memory=False)
    ll = d["geocoded_column"].str.extract(r"\(\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)\s*\)")
    d["lat"], d["lon"] = ll[0], ll[1]
    d.drop(columns="geocoded_column").to_csv(ROOT / "data/interim/dallas_incidents_slim.csv", index=False)
    print(f"{int((v['ori'] == 'TXDPD0000').sum()):,} Dallas PD rows; {len(d):,} city rows, lat and lon for {d['lat'].notna().mean():.1%}")


if __name__ == "__main__":
    main()
