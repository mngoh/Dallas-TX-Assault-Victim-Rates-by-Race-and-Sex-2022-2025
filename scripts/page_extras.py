"""Write out/extra_sections.json: the city public file section and the location section for the page.

NIBRS has no location. The city's public file (Dallas OpenData, Police Incidents) has victim race and coordinates, but
only for non-family assaults with no victim or suspect under 17. The kit runs on that subset from city/analysis.json
(division test, tract model); this script turns those results, the coverage counts and where women live into page
sections. Every number in the text comes from out/city_file_coverage.json, out/city_ages.json,
city/out/results.json or city/out/population.json.

  python scripts/page_extras.py analysis.json   ->  out/extra_sections.json  (read by the kit's build_page.py)
"""
import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.expanduser(os.environ.get("DISPARITY_KIT", "~/.claude/disparity-kit/kit")))
from common import SEX_WORD, Project  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANDS = [("Under 10%", 0, 0.10), ("10% to 25%", 0.10, 0.25), ("25% or more", 0.25, 2)]
COLOR = {"Black": "red", "Hispanic": "blue", "White": "blueLight", "Asian": "muted"}
STEP = {"group only": "Crude", "+ age": "+ age", "+ year": "+ year", "+ district": "+ police division", "+ tract socioeconomics": ["+ tract poverty,", "income, jobs, housing"]}  # two lines so phones do not clip it


def x(v):
    r = round(v, 1)
    return str(int(r)) if r == int(r) else str(r)


def dname(d):
    return "CBD (downtown)" if d == "CBD" else d.title()


def listing(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def main():
    p = Project(sys.argv[1])
    G, S = p.focus
    FL, sexw = p.focus_label, SEX_WORD[S][0]
    groups, others = p.groups, p.others
    cov = p.read_json("city_file_coverage.json")
    ages = p.read_json("city_ages.json")
    C = json.loads((ROOT / "city/out/results.json").read_text())
    cpop = json.loads((ROOT / "city/out/population.json").read_text())
    M, L = C["model"], C["tests"]["location"]
    w0, w1 = p.cfg["window"]["start"][:4], p.cfg["window"]["end"][:4]
    n_city = sum(cov["women_city"][g] for g in groups)
    n_nibrs = sum(cov["women_nibrs"][g] for g in groups)

    # the city public file: what it holds
    share, matched = cov["city_share_of_nibrs_pct"], cov["matched_share_of_nibrs_pct"]
    holds = {"id": "cityShare", "title": "What the city's public file holds",
             "text": f"Of the assaults on {sexw} that Dallas police reported to the FBI, the city's public file holds {min(share.values())}% to {max(share.values())}%: "
                     f"{share[G]}% for {G} {sexw}, " + listing(f"{share[g]}% {g}" for g in others) + ". "
                     f"Filtering the FBI's file the same way (no family or partner assault, no one under 17) keeps {min(matched.values())}% to {max(matched.values())}%. "
                     "The city file holds fewer still, but evenly enough across groups that the ratios agree (Replication, below).",
             "labels": [f"{g} {sexw}" for g in groups],
             "datasets": [{"label": "NIBRS filtered like the city file", "data": [matched[g] for g in groups], "color": "muted"},
                          {"label": "City public file", "data": [share[g] for g in groups], "color": "red"}],
             "ytitle": "% of NIBRS assaults on women"}
    city_section = {"title": "The city's public file",
                    "note": f"Dallas police publish incident data on Dallas OpenData with victim race and locations, but without family violence or any offense with a "
                            f"victim or suspect under 17. For {w0} to {w1} it holds {n_city:,} assaults on {sexw} in the compared groups, against {n_nibrs:,} in the FBI's NIBRS files. "
                            "The rates above use NIBRS. The city file is used for the replication and for the location section below.",
             "boxes": [holds]}

    # where: division test and tract model on the city file's subset
    rated = [d for d in L["districts"] if d["ratio"] is not None]
    lo, hi = min(rated, key=lambda d: d["ratio"]), max(rated, key=lambda d: d["ratio"])
    skipped = [dname(d["district"]) for d in L["districts"] if d["ratio"] is None]
    div = {"id": "divChart", "title": "Inside each police division",
           "text": f"In this subset, {FL}'s rate is higher than other {sexw}'s in every division where it can be rated, from {lo['ratio']}x in {dname(lo['district'])} "
                   f"to {hi['ratio']}x in {dname(hi['district'])}. If {FL} had other {sexw}'s rate in each division, theirs would be {L['expected_if_other_rates']:,} "
                   f"per 100,000 a year, not {L['actual_rate']:,}." + (f" {listing(skipped)} is not rated: too few {G} {sexw} live there." if skipped else ""),
           "labels": [dname(d["district"]) for d in rated],
           "datasets": [{"label": FL, "data": [d["focus_rate"] for d in rated], "color": "red"},
                        {"label": f"Other {sexw}", "data": [d["other_rate"] for d in rated], "color": "blue"}],
           "ytitle": "Victims per 100,000 per year", "tall": True}
    lad = M["ladder"]
    ladder = {"id": "cityLadder", "title": "How much survives adjustment",
              "text": f"Poisson rate models on {M['cells']:,} tract by group by age by year cells, covering {M['coverage']['focus']}% of located {FL} victims. "
                      f"Crude {lad[0]['rate_ratio']}x. Age, year and division leave it at {lad[-2]['rate_ratio']}x. Tract poverty, income, unemployment, renting and density "
                      f"narrow it to {lad[-1]['rate_ratio']}x (95% CI {lad[-1]['ci_low']} to {lad[-1]['ci_high']}): about {M['explained_pct']}% of the crude excess.",
              "labels": [STEP.get(m["model"], m["model"]) for m in lad], "datasets": [{"label": "Rate ratio", "data": [m["rate_ratio"] for m in lad], "color": "red"}],
              "ytitle": f"{FL}'s rate as a multiple of other {sexw}'s", "horizontal": True, "legend": False, "tall": True}
    pw = M["pairwise"]
    pair = {"id": "cityPair", "title": "Each comparison group on its own",
            "text": "Fully adjusted: " + listing(f"{pw[g]['adjusted']['rate_ratio']}x {g} {sexw} (95% CI {pw[g]['adjusted']['ci_low']} to {pw[g]['adjusted']['ci_high']})" for g in pw)
                    + ". Crude in grey.",
            "labels": [f"{g} {sexw}" for g in pw],
            "datasets": [{"label": "Crude", "data": [pw[g]["crude"]["rate_ratio"] for g in pw], "color": "muted"},
                         {"label": "Fully adjusted", "data": [pw[g]["adjusted"]["rate_ratio"] for g in pw], "color": "red"}],
            "ytitle": "Rate ratio"}

    # where women live, by tract poverty (tracts inside DPD divisions)
    tr = [t for t in cpop["tracts"] if t["district"] and t["ses"]["poverty"] is not None]
    dist = {}
    for g in groups:
        tot = sum(sum(t["pop"][g][S]) for t in tr)
        dist[g] = [round(sum(sum(t["pop"][g][S]) for t in tr if a <= t["ses"]["poverty"] < b) / tot * 100, 1) for _, a, b in BANDS]
    live = {"id": "povChart", "title": f"Where {sexw} live, by tract poverty",
            "text": f"{dist[G][2]}% of {G} {sexw} live in census tracts where 25% or more of residents are poor, against "
                    + listing(f"{dist[g][2]}% of {g} {sexw}" for g in others) + ". The tract model compares women in tracts with similar poverty, income, jobs and housing.",
            "labels": [b for b, _, _ in BANDS],
            "datasets": [{"label": f"{g} {sexw}", "data": dist[g], "color": COLOR.get(g, "grey2")} for g in groups],
            "ytitle": f"% of each group's {sexw}"}
    fam = round(sum(cov["removed_by"]["partner"][g] + cov["removed_by"]["other_family"][g] for g in groups) / n_nibrs * 100)
    linked = listing(f"{a['age_known_pct_women']}% in {k} assaults" for k, a in ages.items())
    where = {"title": "Where: non-family assaults, from the city's file",
             "note": f"NIBRS has no location, so this section uses the city's public file: assaults with no family or partner relationship and no one under 17, "
                     f"{cov['women_city'][G]:,} on {FL} and {sum(cov['women_city'][g] for g in others):,} on other {sexw} in the compared groups, {w0} to {w1}. "
                     f"Victim ages are linked from the city's Police Person table ({linked}). It describes that part of the data, not all assaults.",
             "boxes": [div, ladder, pair, live],
             "findings": [{"title": "What the subset shows", "red": True,
                           "text": f"In non-family assaults, {FL}'s rate is {C['ratios']['Hispanic']}x Hispanic, {C['ratios']['White']}x White and {C['ratios']['Asian']}x Asian {sexw}'s. "
                                   f"The gap holds inside every police division. Comparing women in tracts with similar poverty, income, jobs and housing narrows it to "
                                   f"{lad[-1]['rate_ratio']}x. Those conditions are shaped by segregation, so this locates part of the gap in where women live; it does not explain it away."},
                          {"title": "What it cannot show",
                           "text": f"Partner and other family assaults have no public location, and they are {fam}% of the assaults on {sexw} in NIBRS. "
                                   "Whether neighborhood accounts for the same share of those is unknown."}]}

    extra = {"sections": [city_section, where],
             "readme": [["City public file", f"holds {min(share.values())}% to {max(share.values())}% of the assaults on {sexw} in NIBRS ({share[G]}% for {G} {sexw}); "
                                             f"NIBRS filtered the same way keeps {min(matched.values())}% to {max(matched.values())}%"],
                        ["Where (city file, non-family)", f"{FL} {C['ratios']['Hispanic']}x Hispanic, {C['ratios']['White']}x White, {C['ratios']['Asian']}x Asian {sexw}; "
                                                          f"higher in every rated division ({lo['ratio']}x to {hi['ratio']}x); "
                                                          f"model crude {lad[0]['rate_ratio']}x, {lad[-1]['rate_ratio']}x after tract controls (95% CI {lad[-1]['ci_low']} to {lad[-1]['ci_high']})"]]}
    p.write_json("extra_sections.json", extra)


if __name__ == "__main__":
    main()
