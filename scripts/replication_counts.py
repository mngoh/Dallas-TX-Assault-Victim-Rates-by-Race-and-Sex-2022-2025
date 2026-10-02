"""Counts for the replication check: the FBI's NIBRS file against Dallas's own public incident file.

Dallas police publish incidents on Dallas OpenData (Police Incidents, qv6i-rri7), filtered before release. The dataset
description lists sexually oriented offenses and offenses where a victim or suspect is under 17. Family violence is
also missing, though not listed: the file's family-violence flag is never set, and its assault offenses are named
"NON FAMILY VIOLENCE". The analysis uses NIBRS, which holds all of them. To test whether the two sources agree, NIBRS
is filtered the same way and set against the city file: same years, same women, same race rule, same population.

  primary     NIBRS 2022 to 2025, filtered like the city file: women victims of 13A or 13B (individuals), age 17 or over
              or unknown, no partner or family relationship to any offender, no offender under 17 (unknown ages kept).
  secondary   Dallas OpenData Police Incidents 2022 to 2025: women victims (involvement Victim, victim type Individual)
              of NIBRS codes 13A or 13B, by occurrence date.

Race rule in both: Hispanic of any race first (ethnicity, or "Hispanic or Latino" written in the city file's race
column), otherwise the recorded race. A city-file victim listed under both 13A and 13B in one incident (same incident,
race, ethnicity and sex) is counted once in "all", as aggravated, as NIBRS does.

Also writes out/city_file_coverage.json: the city file's count as a share of all NIBRS assaults on women, by group,
and the filter's parts, so the caveats can say how much the public file leaves out and for whom.

  python scripts/replication_counts.py analysis.json   ->  out/replication_counts.json, out/city_file_coverage.json
  then: python ~/.claude/disparity-kit/kit/replicate.py analysis.json
"""
import json
import os
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.expanduser(os.environ.get("DISPARITY_KIT", "~/.claude/disparity-kit/kit")))
from nibrs import reader  # noqa: E402

CITY = "data/interim/dallas_incidents_slim.csv"  # columns of data/raw/dallas_incidents.csv, lat and lon parsed
ZIPS = "data/raw/TX-*.zip"
ORI = "TXDPD0000"
PARTNER = {"SE", "CS", "BG", "HR", "XS", "XR"}
FAMILY = {"PA", "CH", "SB", "OF", "IL", "GP", "GC", "SC", "SP", "SS", "CF"}  # Texas family violence: family, household, dating
CITY_RACE = {"Black": "B", "White": "W", "Asian": "A"}
KIND = {"13A": "aggravated", "13B": "simple"}


def years(a, b):
    a, b = pd.Timestamp(a), pd.Timestamp(b)
    return round(sum(((min(b, pd.Timestamp(y, 12, 31)) - max(a, pd.Timestamp(y, 1, 1))).days + 1) / (366 if y % 4 == 0 else 365)
                     for y in range(a.year, b.year + 1)), 4)


def counts(d, groups):
    cats = {"all": d}
    cats.update({k: d[d["kind"] == k] for k in ("simple", "aggravated")})
    return {c: {g: int((x["group"] == g).sum()) for g in groups} for c, x in cats.items()}


def juvenile_offender_incidents(root, incidents):
    """Incident ids (as strings) with any offender recorded as under 17. Unknown ages do not count."""
    hit = set()
    for z in sorted(root.glob(ZIPS)):
        read = reader(z)
        age_code = read("NIBRS_AGE").set_index("age_id")["age_code"].to_dict()
        off = read("NIBRS_OFFENDER", usecols=["incident_id", "age_id", "age_num"])
        off = off[off["incident_id"].astype(str).isin(incidents)]
        code = off["age_id"].map(age_code)
        age = pd.to_numeric(off["age_num"], errors="coerce").where(~code.isin(["00", "NS"]))
        age[code.isin(["NN", "NB", "BB"])] = 0
        hit |= set(off.loc[age < 17, "incident_id"].astype(str))
    return hit


def main():
    cfg_path = pathlib.Path(sys.argv[1]).resolve()
    root = cfg_path.parent
    cfg = json.loads(cfg_path.read_text())
    S, groups, rm = cfg["focus"].get("sex", "F"), cfg["groups"], cfg["race_map"]
    w0, w1 = cfg["window"]["start"], cfg["window"]["end"]

    # NIBRS: the analysis's own victim files, then the city's filter
    nib = pd.concat([pd.read_csv(root / s["path"], dtype=str, keep_default_na=False).assign(kind=s["kind"]) for s in cfg["incidents"]])
    nib = nib[(nib["incident_date"].str[:10] >= w0) & (nib["incident_date"].str[:10] <= w1) & (nib["sex"] == S)].copy()
    nib["group"] = nib["race_group"].map(rm)
    rel = nib["relationship"].str.split(";").apply(set)
    age = pd.to_numeric(nib["age"], errors="coerce")
    juv = juvenile_offender_incidents(root, set(nib["incident_id"]))
    parts = pd.DataFrame({"victim_under_17": age < 17,
                          "partner": rel.apply(lambda s: bool(s & PARTNER)),
                          "other_family": rel.apply(lambda s: bool(s & FAMILY) and not s & PARTNER),
                          "offender_under_17": nib["incident_id"].isin(juv)}, index=nib.index)
    matched = nib[~parts.any(axis=1)]

    # city file
    city = pd.read_csv(root / CITY, dtype=str, keep_default_na=False, low_memory=False,
                       usecols=["incidentnum", "servnumid", "date1", "involvement", "victimtype", "comprace", "compethnicity", "compsex", "nibrs_code", "offincident"])
    city = city[(city["involvement"] == "Victim") & (city["victimtype"] == "Individual") & (city["date1"].str[:10] >= w0) & (city["date1"].str[:10] <= w1)
                & (city["compsex"] == {"F": "Female", "M": "Male"}[S])].copy()
    hisp = (city["compethnicity"] == "Hispanic or Latino") | city["comprace"].isin(["Hispanic or Latino", "H"])
    city["group"] = pd.Series(np.where(hisp, "H", city["comprace"].map(CITY_RACE)), index=city.index).map(rm)
    # assaults still classed as preliminary investigations carry NIBRS code 999 in the city file: left out, reported as a sensitivity
    prelim = city[city["offincident"].str.contains("PRELIMINARY INVESTIGATION") & city["offincident"].str.contains("ASSAULT|DEADLY CONDUCT")]
    city = city[city["nibrs_code"].isin(KIND)].copy()
    city["kind"] = city["nibrs_code"].map(KIND)
    person = ["incidentnum", "comprace", "compethnicity", "compsex"]
    both = city.sort_values("kind").duplicated(person, keep="first") & city.groupby(person)["kind"].transform("nunique").gt(1)
    city_all = city[~both]

    y = years(w0, w1)
    sources = {"primary": {"label": f"NIBRS filtered like the city file, {w0[:4]} to {w1[:4]}", "years": y, "counts": counts(matched, groups)},
               "secondary": {"label": f"City public file, {w0[:4]} to {w1[:4]}", "years": y, "counts": counts(city, groups)}}
    sources["secondary"]["counts"]["all"] = counts(city_all, groups)["all"]
    nib_all = counts(nib, groups)["all"]
    pop = json.loads((root / "out" / "population.json").read_text())["city"]
    G = cfg["focus"]["group"]
    rate = lambda n, g: round(n / pop[g][S] / y * 1e5)  # rounded like replicate.py, so the note matches out/replication.json
    ratios = lambda c: {g: round(rate(c[G], G) / rate(c[g], g), 2) for g in groups if g != G and c[g]}
    pre = {g: int((prelim["group"] == g).sum()) for g in groups}
    with_pre = {g: sources["secondary"]["counts"]["all"][g] + pre[g] for g in groups}
    m_tot, c_tot = sum(sources["primary"]["counts"]["all"].values()), sum(sources["secondary"]["counts"]["all"].values())
    short = round((1 - c_tot / m_tot) * 100)
    r_pre = ratios(with_pre)
    spec = {"sources": sources,
            "definition_notes": f"Dallas police publish their incidents with family violence, and offenses where a victim or suspect is under 17, removed. NIBRS {w0[:4]} to {w1[:4]} "
                                "is filtered the same way here (women 17 or older, no partner or family relationship to any offender, no offender under 17) and set against "
                                "the city file over the same years. Same women, same race rule (Hispanic of any race first), same population. "
                                f"The city file still holds {short}% fewer women than NIBRS filtered this way, so it leaves out more than these rules do, "
                                "but the shortfall is close to even across groups. "
                                f"{sum(pre.values()):,} more women in the city file are in assaults still classed as preliminary investigations, outside codes 13A and 13B; "
                                "counting them moves the city file's ratios to " + ", ".join(f"{v}x {g}" for g, v in r_pre.items()) + ". "
                                f"A woman listed under both 13A and 13B in one city-file incident is counted once in the total, as aggravated ({int(both.sum())} in this period).",
            "nibrs_all_counts": nib_all}
    (root / "out" / "replication_counts.json").write_text(json.dumps(spec, indent=1) + "\n")

    keep = lambda m: {g: int(m[nib["group"] == g].sum()) for g in groups}
    cov = {"women_nibrs": nib_all, "women_nibrs_matched": sources["primary"]["counts"]["all"], "women_city": sources["secondary"]["counts"]["all"],
           "city_share_of_nibrs_pct": {g: round(sources["secondary"]["counts"]["all"][g] / nib_all[g] * 100, 1) for g in groups},
           "matched_share_of_nibrs_pct": {g: round(sources["primary"]["counts"]["all"][g] / nib_all[g] * 100, 1) for g in groups},
           "city_vs_matched_pct": {g: round((sources["secondary"]["counts"]["all"][g] / sources["primary"]["counts"]["all"][g] - 1) * 100, 1) for g in groups},
           "removed_by": {k: keep(parts[k]) for k in parts.columns},
           "removed_any": keep(parts.any(axis=1)),
           "city_women_other_race": {k: int(v) for k, v in city.loc[city["group"].isna(), "comprace"].replace("", "(blank)").value_counts().items()},
           "city_both_kinds": int(both.sum()),
           "city_short_of_matched_pct": short,
           "preliminary": {"women": pre, "ratios_with": r_pre, "ratios_without": ratios(sources["secondary"]["counts"]["all"])}}
    (root / "out" / "city_file_coverage.json").write_text(json.dumps(cov, indent=1) + "\n")
    print("wrote out/replication_counts.json and out/city_file_coverage.json")
    for k, s in sources.items():
        print(k, s["label"], s["years"], s["counts"]["all"])
    print("NIBRS all", nib_all)
    print(json.dumps({k: cov[k] for k in ("city_share_of_nibrs_pct", "matched_share_of_nibrs_pct", "city_vs_matched_pct", "removed_any", "city_women_other_race")}, indent=1))


if __name__ == "__main__":
    main()
