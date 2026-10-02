"""Dallas-specific checks the kit cannot run on NIBRS, and the caveats and headline they produce.

  ethnicity bound      NIBRS records Hispanic ethnicity apart from race. White-race victims with unknown ethnicity are
                       counted as White; here they are moved to Hispanic, or split in the known proportion.
  missing race         NIBRS has no location, so victims with unknown race are spread over the four groups like known
                       victims of the same assault type and premises, and the ratios recomputed.
  relationship         unknown or blank relationship by group: the partner flag is a lower bound.
  agencies             assault victims recorded by other agencies in Dallas County, left out.
  exclusions           officer victims, intimidation, unknown age, groups not compared.
  premises             Dallas police's use of NIBRS location codes against other large Texas departments, and the
                       city file's own premise names.
  city file            how much of NIBRS the city's public file holds (scripts/replication_counts.py), the age link
                       (scripts/city_ages.py), and the location results on that subset (city/out/results.json).
  stability            which comparison moves most between sources and across years.
  poverty              where women of each group live, by tract poverty (tracts inside DPD divisions).

Writes out/dallas_checks.json and regenerates `extra_caveats`, `headline` and `question` in analysis.json from it,
so every number in them comes from an output.

  python scripts/dallas_checks.py analysis.json
"""
import io
import json
import os
import pathlib
import re
import sys
import zipfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.expanduser(os.environ.get("DISPARITY_KIT", "~/.claude/disparity-kit/kit")))
from common import Project, load_incidents, year_spans  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
ORI = "TXDPD0000"
AGENCY = {"TX0575300": "DART police", "TX057519E": "Baylor Health Care System police", "TX0575400": "Dallas ISD police",
          "TX0570000": "Dallas County Sheriff", "TX0572600": "UT Southwestern police", "TX0575000": "Parkland (county hospital district) police",
          "TX057529E": "SMU police", "TX057819E": "Texas Health police", "TX0579000": "Dallas College police", "TX057829E": "Dallas Baptist University police"}
PEERS = {"TXHPD0000": "Houston", "TXSPD0000": "San Antonio", "TX2201200": "Fort Worth", "TX2270100": "Austin", "TX0710200": "El Paso"}  # the five other largest city police departments in Texas
NOT_COMPARED = {"I": "American Indian or Alaska Native", "P": "Native Hawaiian or Pacific Islander"}
POOR = 0.25


def ratio(a, b):
    return round(a / b, 2) if b else None


def listing(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def pct(a, b):
    return round(a / b * 100, 1) if b else None


def x1(v):
    r = round(v, 1)
    return str(int(r)) if r == int(r) else str(r)


def premises_by_agency(w0, w1):
    """Share of 13A and 13B offenses by NIBRS location, per agency, from the state files."""
    rows = []
    for z in sorted(ROOT.glob("data/raw/TX-*.zip")):
        zf = zipfile.ZipFile(z)
        names = {pathlib.PurePosixPath(n).name.lower(): n for n in zf.namelist()}
        rd = lambda t, **kw: pd.read_csv(io.BytesIO(zf.read(names[t.lower() + ".csv"])), low_memory=False, **kw).rename(columns=str.lower)
        ag = rd("agencies").set_index("agency_id")["ori"]
        inc = rd("NIBRS_incident", usecols=lambda c: c.lower() in ("incident_id", "agency_id", "incident_date"))
        inc["ori"] = inc["agency_id"].map(ag)
        inc = inc[inc["ori"].isin([ORI, *PEERS]) & inc["incident_date"].astype(str).str[:10].between(w0, w1)]
        off = rd("NIBRS_OFFENSE", usecols=lambda c: c.lower() in ("incident_id", "offense_code", "location_id"))
        off = off[off["offense_code"].isin(["13A", "13B"])].merge(inc[["incident_id", "ori"]], on="incident_id")
        loc = rd("NIBRS_LOCATION_TYPE").set_index("location_id")["location_name"]
        off["location"] = off["location_id"].map(loc)
        rows.append(off[["ori", "location"]])
    d = pd.concat(rows, ignore_index=True)
    share = (pd.crosstab(d["location"], d["ori"], normalize="columns") * 100).round(1)
    keep = ["Commercial/Office Building", "Field/Woods", "Residence/Home"]
    return {loc: {o: float(share.loc[loc, o]) for o in share.columns} for loc in keep}, d["ori"].value_counts().to_dict()


def main():
    p = Project(sys.argv[1])
    G, S = p.focus
    pop = p.read_json("population.json")["city"]
    R = p.read_json("results.json")
    _, years = year_spans(p)
    rate = lambda n, g: round(n / pop[g][S] / years * 1e5)  # rounded like the kit, so "as mapped" matches results.json
    start, end = p.window()
    w0, w1 = f"{start:%Y-%m-%d}", f"{end:%Y-%m-%d}"
    raw = pd.concat([pd.read_csv(p.path(s["path"]), dtype={"victim_id": str, "relationship": str}).assign(kind=s["kind"]) for s in p.cfg["incidents"]])
    raw["date"] = pd.to_datetime(raw["incident_date"])
    raw = raw[(raw["date"] >= start) & (raw["date"] <= end)]
    women = raw[raw["sex"] == S]
    rm = p.cfg["race_map"]
    out = {}

    # ethnicity bound: White-race women with unknown or unspecified ethnicity
    w = women[women["race"] == "W"]
    w_h, w_n, w_u = int((w["ethnicity"] == "H").sum()), int((w["ethnicity"] == "N").sum()), int(w["ethnicity"].isin(["U", "X"]).sum())
    share_h = w_h / (w_h + w_n)
    n = {g: int((women["race_group"].map(rm) == g).sum()) for g in p.groups}
    scen = {"as mapped": (n["Hispanic"], n["White"]),
            "unknown ethnicity left out": (n["Hispanic"], n["White"] - w_u),
            "split in known proportion": (n["Hispanic"] + share_h * w_u, n["White"] - share_h * w_u),
            "all Hispanic": (n["Hispanic"] + w_u, n["White"] - w_u)}
    fr = rate(n[G], G)
    sc = {k: {"Hispanic": ratio(fr, rate(h, "Hispanic")), "White": ratio(fr, rate(wh, "White"))} for k, (h, wh) in scen.items()}
    out["ethnicity"] = {"white_race_women": len(w), "white_unknown_ethnicity": w_u, "white_unknown_pct": pct(w_u, len(w)),
                        "hispanic_share_where_known_pct": round(share_h * 100, 1),
                        "all_unknown_ethnicity_pct": round(float(women["ethnicity"].isin(["U", "X"]).mean() * 100), 1),
                        "black_race_hispanic": int(((women["race"] == "B") & (women["ethnicity"] == "H")).sum()),
                        "scenarios": sc,
                        "hispanic_range": [min(v["Hispanic"] for v in sc.values()), max(v["Hispanic"] for v in sc.values())],
                        "white_range": [min(v["White"] for v in sc.values()), max(v["White"] for v in sc.values())]}

    # missing race, spread inside cells of type x premises
    df = load_incidents(p)
    fs = df[df["sex"] == S].copy()
    fs["race_raw"] = raw.set_index("victim_id").reindex(fs["id"].astype(str))["race_group"].values
    fs["cell"] = fs["kind"] + "|" + fs["premise"].fillna("blank").astype(str)
    counts = {g: 0.0 for g in p.groups}
    for _, c in fs.groupby("cell"):
        known = c["race"].value_counts()
        unknown = int((c["race"].isna() & ~c["race_raw"].isin(list(NOT_COMPARED))).sum())
        tot = sum(known.get(g, 0) for g in p.groups)
        for g in p.groups:
            counts[g] += known.get(g, 0) + (unknown * known.get(g, 0) / tot if tot else 0)
    rr = {g: rate(counts[g], g) for g in p.groups}
    out["missing_race"] = {"unknown_women": int((fs["race"].isna() & ~fs["race_raw"].isin(list(NOT_COMPARED))).sum()),
                           "ratios_redistributed": {g: ratio(rr[G], rr[g]) for g in p.others}, "ratios_as_mapped": R["ratios"]}

    # relationship unknown or blank, by group
    wg = women.assign(group=women["race_group"].map(rm)).dropna(subset=["group"])
    rel = wg["relationship"].fillna("").str.split(";").apply(set)
    unk = rel.apply(lambda s: s <= {"RU", ""})
    out["relationship_unknown_pct"] = {g: round(float(v.mean() * 100), 1) for g, v in unk.groupby(wg["group"])}

    # exclusions, from the flattened file
    v = pd.read_csv(ROOT / "data/interim/victim_offenses.csv", low_memory=False, dtype={"age_num": str, "age_code": str})
    v = v[pd.to_datetime(v["incident_date"]).between(start, end)]
    core = v["offense_code"].isin(["13A", "13B"])
    ind = v["victim_type"] == "Individual"
    other = v[core & ind & (v["ori"] != ORI)].drop_duplicates("victim_id")["ori"].value_counts()
    out["excluded"] = {"other_agencies": {AGENCY.get(o, o): int(k) for o, k in other.items()},
                       "other_agencies_total": int(other.sum()),
                       "officer_victims": int(v[core & (v["ori"] == ORI) & (v["victim_type"] == "Law Enforcement Officer")]["victim_id"].nunique()),
                       "intimidation_victims": int(v[(v["offense_code"] == "13C") & (v["ori"] == ORI) & ind]["victim_id"].nunique()),
                       "age_unknown": int(raw["age"].isna().sum()),
                       "not_rated_race": {k: int((raw["race_group"] == k).sum()) for k in NOT_COMPARED},
                       "victims_under_17": int((raw["age"] < 17).sum()),
                       "women_under_17": int((women["age"] < 17).sum()),
                       "resident_blank_pct": round(float(raw["resident_status"].isna().mean() * 100), 1)}

    # premises: Dallas police's location codes against other large Texas departments
    share, n_off = premises_by_agency(w0, w1)
    city = pd.concat([pd.read_csv(ROOT / f"data/city/dallas_city_{k}_aged.csv", dtype=str, keep_default_na=False) for k in ("simple", "aggravated")])
    city = city[city["date1"].str[:10].between(w0, w1)]
    cp = city["premise"].value_counts(normalize=True) * 100
    peers = {PEERS[o]: {loc: share[loc][o] for loc in share} for o in PEERS if o in share["Residence/Home"]}
    out["premises"] = {"dallas": {loc: share[loc][ORI] for loc in share}, "peers": peers, "assault_offenses": {PEERS.get(o, "Dallas"): int(k) for o, k in n_off.items()},
                       "city_file_pct": {k: round(float(cp.get(k, 0)), 1) for k in ["Apartment Complex/Building", "Apartment Residence", "Apartment Parking Lot", "Outdoor Area Public/Private", "Business Office", "Commercial Property Occupied/Vacant"]}}

    # the city file: coverage, age link, location results on its subset
    cov = p.read_json("city_file_coverage.json")
    ages = p.read_json("city_ages.json")
    C = json.loads((ROOT / "city/out/results.json").read_text())
    linked = sum(a["rows_in_window"] * a["age_known_pct_women"] / 100 for a in ages.values())
    out["city_file"] = {"share_of_nibrs_pct": cov["city_share_of_nibrs_pct"], "short_of_matched_pct": cov["city_short_of_matched_pct"],
                        "women_city": cov["women_city"], "age_known_pct_women": {k: a["age_known_pct_women"] for k, a in ages.items()},
                        "ratios": C["ratios"], "model": C.get("model"), "location": C["tests"].get("location")}

    # where women live: tract poverty, tracts inside DPD divisions
    cpop = json.loads((ROOT / "city/out/population.json").read_text())
    tr = [t for t in cpop["tracts"] if t["district"] and t["ses"]["poverty"] is not None]
    live = {}
    for g in p.groups:
        tot = sum(sum(t["pop"][g][S]) for t in tr)
        poor = sum(sum(t["pop"][g][S]) for t in tr if t["ses"]["poverty"] >= POOR)
        live[g] = pct(poor, tot)
    out["women_in_poor_tracts_pct"] = live

    # stability: across sources by type, and first half against second half of the window
    rep = p.read_json("replication.json")
    T = R["tests"]["time"]
    yrs = sorted(T)
    half = lambda ys: {g: ratio(sum(T[y][G] for y in ys), sum(T[y][g] for y in ys)) for g in p.others}
    a, b = half(yrs[:len(yrs) // 2]), half(yrs[len(yrs) // 2:])
    out["stability"] = {"halves": {"first": a, "second": b, "change_pct": {g: round((b[g] / a[g] - 1) * 100) for g in p.others}, "years": [yrs[:len(yrs) // 2], yrs[len(yrs) // 2:]]},
                        "sources": {cat: {g: v["change_pct"] for g, v in c.items()} for cat, c in rep["comparison"].items()}}
    moves = {g: max([abs(out["stability"]["halves"]["change_pct"][g])] + [abs(c[g]) for c in out["stability"]["sources"].values() if c.get(g) is not None]) for g in p.others}
    worst = max(moves, key=moves.get)
    out["stability"]["least_stable"] = {"group": worst, "max_move_pct": moves[worst], "others_max_pct": max(m for g, m in moves.items() if g != worst),
                                        "victims": n[worst]}
    p.write_json("dallas_checks.json", out)

    # caveats, generated from the checks above
    e, m, xx, pr, cf, st = out["ethnicity"], out["missing_race"], out["excluded"], out["premises"], out["city_file"], out["stability"]
    release = p.read_json("population.json")["release"]
    acs_year = int(re.search(r"\d{4}", release).group())
    ru = out["relationship_unknown_pct"]
    flag = R["tests"]["flags"]["partner"]
    M, L = cf["model"], cf["location"]
    lad = M["ladder"]
    peer_hi = lambda loc: max(v[loc] for v in pr["peers"].values())
    home = [v["Residence/Home"] for v in pr["peers"].values()]
    ls = st["least_stable"]
    agencies = ", ".join(f"{k} {v:,}" for k, v in xx["other_agencies"].items() if v >= 10)
    caveats = [
        ["Victims have no location",
         "The FBI's NIBRS files record no address or police division, so the location test and the tract model run on the city's own public file instead "
         "(the Where section). That file holds only non-family assaults on victims 17 and older, so those results describe that part of the data, not all assaults."],
        ["The city's public file leaves most assaults out",
         "Dallas police publish their incident data without family violence or any offense with a victim or suspect under 17. The age rule is in the dataset's "
         "description. The family violence rule is not, but the file's family-violence flag is not set on any record. "
         f"For {w0[:4]} to {w1[:4]} the public file holds {cf['share_of_nibrs_pct'][G]}% of the assaults on {G} women that Dallas police reported to the FBI, against "
         + listing(f"{cf['share_of_nibrs_pct'][g]}% for {g}" for g in p.others) + " women. This analysis uses the FBI's NIBRS files, which hold them all."],
        ["Agencies in the file",
         f"Only the Dallas Police Department. Other agencies in Dallas County recorded {xx['other_agencies_total']:,} assault victims in these years ({agencies}). "
         "Some work partly outside the city, and some began reporting partway through, so they are left out. Assaults only they recorded are missing."],
        ["Policing and reporting",
         "Police data reflects where officers patrol and who calls them. This data cannot separate more policing or more reporting from more assaults."],
        ["Hispanic ethnicity",
         f"NIBRS records ethnicity apart from race, and it is unknown or unspecified for {e['all_unknown_ethnicity_pct']}% of women victims. "
         f"{e['white_unknown_ethnicity']:,} women recorded as White ({e['white_unknown_pct']}%) have unknown ethnicity; where it is known, {e['hispanic_share_where_known_pct']}% of White-race women are Hispanic. "
         f"They are counted as White. If they were all Hispanic, Black women's rate would be {e['scenarios']['all Hispanic']['Hispanic']}x Hispanic women's instead of {R['ratios']['Hispanic']}x, "
         f"and {e['scenarios']['all Hispanic']['White']}x White women's instead of {R['ratios']['White']}x. "
         f"Hispanic of any race counts as Hispanic, so {e['black_race_hispanic']:,} women recorded as Black and Hispanic are in the Hispanic group."],
        ["Missing race",
         f"{m['unknown_women']:,} women victims have unknown race. Spread over the four groups like known victims of the same assault type and premises, "
         + ("they do not move the ratios (" + listing(f"{R['ratios'][g]}x {g}" for g in p.others) + ")."
            if m["ratios_redistributed"] == {g: R["ratios"][g] for g in p.others} else
            "the ratios move to " + listing(f"{m['ratios_redistributed'][g]}x {g}" for g in p.others) + " from " + listing(f"{R['ratios'][g]}x" for g in p.others) + ".")],
        ["Intimate partner is a lower bound",
         "Partner assaults are identified from the victim-offender relationship, which is unknown or blank for "
         + listing(f"{ru[g]}% of {g}" for g in p.groups) + " women victims. "
         f"Partner assault is {flag['share'][G]}% of assaults on {G} women, and " + listing(f"{flag['share'][g]}% on {g}" for g in p.others) + " women."],
        ["Premises codes",
         f"Dallas police file {pr['dallas']['Commercial/Office Building']}% of assaults under the FBI's commercial or office building category and {pr['dallas']['Field/Woods']}% under field or woods, "
         f"against {peer_hi('Commercial/Office Building')}% or less and {peer_hi('Field/Woods')}% or less in " + listing(pr["peers"]) + ", the five other largest city police departments in Texas. "
         f"Their own records list apartment complexes ({pr['city_file_pct']['Apartment Complex/Building']}% of assaults in the city file) and outdoor areas "
         f"({pr['city_file_pct']['Outdoor Area Public/Private']}%) as premises, and NIBRS has no such categories, so these two most likely hold them. "
         f"Home is lower to match: {pr['dallas']['Residence/Home']}% of assaults, against {min(home)}% to {max(home)}% elsewhere."],
        ["What is counted",
         f"Aggravated (13A) and simple (13B) assault reported by the Dallas Police Department, individual victims of any age, {xx['victims_under_17']:,} of them under 17. "
         f"Non-fatal shootings are aggravated assaults in NIBRS and are included. Left out: {xx['officer_victims']:,} assaults on officers; "
         f"{xx['intimidation_victims']:,} intimidation victims (threats with no attack). {xx['not_rated_race']['I']} American Indian or Alaska Native and "
         f"{xx['not_rated_race']['P']} Native Hawaiian or Pacific Islander victims are counted in the totals but not compared, because counts this small give unstable rates. "
         f"{xx['age_unknown']} victims with unknown age fall out of the age test only."],
        ["Window and population",
         f"Victims cover {start:%B %Y} to {end:%B %Y}; the population is the {release} estimate, an average over {acs_year - 4} to {acs_year}."],
        ["Residents are the denominator",
         f"Dallas draws commuters and visitors, and rates divide by residents only. NIBRS resident status is blank for {xx['resident_blank_pct']}% of victims here, "
         "so victims who live elsewhere cannot be separated."],
        ["Ages in the city file",
         "The city's incident file has no victim age. In the Where section, ages come from the city's Police Person table, linked by incident, race, ethnicity and sex. "
         + " and ".join(f"{v}% of women in {k} assaults" for k, v in cf["age_known_pct_women"].items()) + " have a linked age; the rest drop out of the model only."],
        ["Neighborhood is not neutral",
         f"Police division and tract poverty, income, unemployment and housing are shaped by segregation and disinvestment. {live_line(out['women_in_poor_tracts_pct'], p.groups)} "
         f"In the city file's subset, tract socioeconomics narrow the gap from {lad[-2]['rate_ratio']}x to {lad[-1]['rate_ratio']}x. "
         "Where a control narrows a gap, the gap has been located, not explained away."],
        ["Least stable comparison",
         f"The {ls['group']} comparison rests on {ls['victims']:,} {ls['group']} women victims. Between the two sources and across years it moved up to {ls['max_move_pct']}%, "
         f"against {ls['others_max_pct']}% or less for the others, so it is left out of the headline."],
    ]
    cfg = json.loads(p.config_path.read_text())
    cfg["extra_caveats"] = caveats

    # headline and question, generated. Ranges span the race-coding worst case, the ethnicity scenarios and the ratios as mapped.
    r, ty = R["ratios"], R["tests"]["type"]
    span = {g: [r[g], R["race_coding_bound"]["ratios_worst_case"][g]] + [v[g] for v in e["scenarios"].values()] for g in ("Hispanic", "White")}
    rng = lambda g: (f"about {x1(min(span[g]))}" if x1(min(span[g])) == x1(max(span[g])) else f"{x1(min(span[g]))} to {x1(max(span[g]))}")
    std = R["tests"]["age"]["standardized"]
    age_note = "and age does not explain it" if all(std[G] / std[g] >= r[g] for g in ("Hispanic", "White")) else "and age explains part of it"
    widest = max(ty, key=lambda k: ty[k][G] / ty[k]["White"])
    kl = cfg.get("kind_labels", {}).get(widest, widest).lower()
    out["headline_ranges"] = {g: [min(v), max(v)] for g, v in span.items()}
    p.write_json("dallas_checks.json", out)
    cfg["headline"] = (f"Black women in Dallas are assaulted at {rng('Hispanic')} times the rate of Hispanic women and {rng('White')} times the rate of White women, {age_note}. "
                       f"The gap is widest for {kl}. Where locations are known, in the city's own records of non-family assaults, comparing women in similar "
                       f"neighborhoods narrows it from {x1(lad[0]['rate_ratio'])} to {x1(lad[-1]['rate_ratio'])} times.")
    cfg["question"] = "Are Black women in Dallas assaulted at a higher rate than Hispanic, White and Asian women, and do the plain explanations account for it?"
    p.config_path.write_text(json.dumps(cfg, indent=1, ensure_ascii=False) + "\n")
    print("updated extra_caveats, headline and question in", p.config_path.name)
    print(cfg["headline"])
    print(json.dumps({k: out[k] for k in ("ethnicity", "missing_race", "relationship_unknown_pct", "excluded", "premises", "women_in_poor_tracts_pct", "stability")}, indent=1))


def live_line(live, groups):
    return (f"{live['Black']}% of Black women live in census tracts where 25% or more of residents are poor, against "
            + listing(f"{live[g]}% of {g} women" for g in groups if g != "Black") + ".")


if __name__ == "__main__":
    main()
