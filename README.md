# Assault victims in Dallas

Who gets assaulted in Dallas, as rates rather than counts: victims of simple and aggravated assault reported by the Dallas Police Department, 2022 to 2025, by race and sex, against ACS population. It is the Dallas companion to the Los Angeles ([Los-Angeles-CA-Assault-Victim-Rates-by-Race-and-Sex-2020-2023](https://github.com/mngoh/Los-Angeles-CA-Assault-Victim-Rates-by-Race-and-Sex-2020-2023)), DC ([DC-Assault-Victims-by-Race-and-Sex-2022-2025](https://github.com/mngoh/DC-Assault-Victims-by-Race-and-Sex-2022-2025)) and Baltimore ([Baltimore-MD-Assault-Victim-Rates-by-Race-and-Sex-2022-2024](https://github.com/mngoh/Baltimore-MD-Assault-Victim-Rates-by-Race-and-Sex-2022-2024)) analyses and uses the same method, packaged as [disparity-kit](https://github.com/mngoh/disparity-kit). It was started from the city's name with the kit's `/new-city` skill.

The full page is `index.html`.

## Results

Every number below is generated from `out/results.json`, `out/dallas_checks.json`, `out/replication.json`, `out/extra_sections.json` and `city/out/results.json`.

<!-- results:start -->
**Black women's reported assault rate in Dallas is 2.1 to 2.3 times Hispanic women's and 3.6 to 4 times White women's, and age does not explain it. The gap is widest for aggravated assault. Where locations are known, in the city's own records of non-family assaults, comparing women in similar neighborhoods narrows it from 2.7 to 2.2 times.**

Rates per 100,000 residents a year, 2022-01-01 to 2025-12-31:

| Group | Women | Men |
|---|---|---|
| Black | 3,798 | 2,506 |
| Hispanic | 1,679 | 1,140 |
| White | 972 | 828 |
| Asian | 281 | 357 |

Tests:

- Age: standardized, Black women 3,966 vs 1,664 Hispanic, 987 White, 252 Asian.
- Type: aggravated assault 2.6 times Hispanic, 5.9 times White, 19.9 times Asian; simple assault 2.2 times Hispanic, 3.5 times White, 12.2 times Asian.
- Time: 4,375, 3,747, 3,577, 3,492.
- Premises: Home 47.9% vs 52.3%, Commercial/Office 19.5% vs 14.3%, Street & Sidewalk 9.9% vs 10.5% (Black women vs other women).
- Weapons: Firearm 17.2% vs 13.3%, Knife or cutting 3.4% vs 2.8%, Blunt object or vehicle 0.7% vs 0.6%, Hands, fists, feet 71.1% vs 76.2%, Other or unknown 7.6% vs 7.0% (Black women vs other women).
- Intimate partner: 37.5% of assaults on Black women (43.7% Hispanic, 41.5% White, 44.2% Asian); ratios with it 1.9x Hispanic, 3.5x White, 11.5x Asian; without it 2.5x Hispanic, 4.2x White, 15.1x Asian.
- City public file: holds 15.0% to 21.2% of the assaults on women in NIBRS (17.1% for Black women); NIBRS filtered the same way keeps 28.6% to 39.2%.
- Where (city file, non-family): Black women 2.59x Hispanic, 3.31x White, 10.87x Asian women; higher in every rated division (1.96x to 4.75x); model crude 2.74x, 2.18x after tract controls (95% CI 2.01 to 2.36).

Replication: Hispanic 2.5x then 2.58x; White 3.15x then 3.32x; Asian 11.21x then 10.83x.

Caveats:

- This shows what, not why: The data says the reported assault rate for Black women is higher. It does not say why. Nothing here measures causes, offenders or circumstances.
- Reported crimes only: Every number is a report that reached the police. Willingness to report, and recording practice, differ by group, area and time.
- Reports, not people: Rates count reports. Someone assaulted twice counts twice, so a rate is not the share of people assaulted.
- Exposure is not population: Rates divide by where people live, not where they spend time.
- Who is recorded as Black: Race is recorded by officers; the population counts people who are Black alone. There are 7% more people who are Black alone or in combination. If multiracial victims are recorded as Black, the worst case is 2.11x Hispanic, 3.64x White, 12.6x Asian instead of 2.26x, 3.91x, 13.52x.
- Overlapping groups: 1.3% of Black residents are also Hispanic, so they sit in both denominators.
- Who is counted: 261 victims are left out of the rates: their sex is unknown, or their race is unknown or outside the compared groups. Race is unknown or outside the groups for 0.2% of women and 0.4% of men.
- What this number measures: Police reports, not how often women are hurt. In the national victimization survey, which counts assaults whether or not police learned of them, Black and White women describe being assaulted at about the same rate nationally and about 1.5 to 2 times in large cities. A follow-up (Police-Records-vs-Survey-Assault-Victims-by-Race-and-Sex-2015-2025, on GitHub) tested why police records differ more: not reporting rates, not (or only a little) how police write up a call, not the same women counted repeatedly, but largely where assaults happen and who calls. Hospital emergency departments, which do not depend on a call to police, see a gap like the police one (about 4.6 times for women in 2021 to 2022), which points to the survey undercounting assaults on Black women.
- Victims have no location: The FBI's NIBRS files record no address or police division, so the location test and the tract model run on the city's own public file instead (the Where section). That file holds only non-family assaults on victims 17 and older, so those results describe that part of the data, not all assaults.
- The city's public file leaves most assaults out: Dallas police publish their incident data without family violence or any offense with a victim or suspect under 17. The age rule is in the dataset's description. The family violence rule is not, but the file's family-violence flag is not set on any record. For 2022 to 2025 the public file holds 17.1% of the assaults on Black women that Dallas police reported to the FBI, against 15.0% for Hispanic, 20.2% for White and 21.2% for Asian women. This analysis uses the FBI's NIBRS files, which hold them all.
- Agencies in the file: Only the Dallas Police Department. Other agencies in Dallas County recorded 4,244 assault victims in these years (DART police 1,149, Baylor Health Care System police 1,088, Dallas ISD police 745, Dallas County Sheriff 484, UT Southwestern police 362, Parkland (county hospital district) police 325, SMU police 73, Dallas College police 10). Some work partly outside the city, and some began reporting partway through, so they are left out. Assaults only they recorded are missing.
- Policing and reporting: Police data reflects where officers patrol and who calls them. This data cannot separate more policing or more reporting from more assaults.
- Hispanic ethnicity: NIBRS records ethnicity apart from race, and it is unknown or unspecified for 1.0% of women victims. 223 women recorded as White (0.9%) have unknown ethnicity; where it is known, 72.5% of White-race women are Hispanic. They are counted as White. If they were all Hispanic, Black women's rate would be 2.23x Hispanic women's instead of 2.26x, and 4.04x White women's instead of 3.91x. Hispanic of any race counts as Hispanic, so 332 women recorded as Black and Hispanic are in the Hispanic group.
- Missing race: 20 women victims have unknown race. Spread over the four groups like known victims of the same assault type and premises, they do not move the ratios (2.26x Hispanic, 3.91x White and 13.52x Asian).
- Intimate partner is a lower bound: Partner assaults are identified from the victim-offender relationship, which is unknown or blank for 13.6% of Black, 13.5% of Hispanic, 13.3% of White and 16.3% of Asian women victims. Partner assault is 37.5% of assaults on Black women, and 43.7% on Hispanic, 41.5% on White and 44.2% on Asian women.
- Premises codes: Dallas police file 16.3% of assaults under the FBI's commercial or office building category and 5.2% under field or woods, against 0.9% or less and 0.6% or less in Houston, San Antonio, Fort Worth, Austin and El Paso, the five other largest city police departments in Texas. Their own records list apartment complexes (12.9% of assaults in the city file) and outdoor areas (8.5%) as premises, and NIBRS has no such categories, so these two most likely hold them. Home is lower to match: 45.0% of assaults, against 50.0% to 68.0% elsewhere.
- What is counted: Aggravated (13A) and simple (13B) assault reported by the Dallas Police Department, individual victims of any age, 6,282 of them under 17. Non-fatal shootings are aggravated assaults in NIBRS and are included. Left out: 640 assaults on officers; 16,389 intimidation victims (threats with no attack). 90 American Indian or Alaska Native and 107 Native Hawaiian or Pacific Islander victims are counted in the totals but not compared, because counts this small give unstable rates. 282 victims with unknown age fall out of the age test only.
- Window and population: Victims cover January 2022 to December 2025; the population is the ACS 2024 5-year estimate, an average over 2020 to 2024.
- Residents are the denominator: Dallas draws commuters and visitors, and rates divide by residents only. NIBRS resident status is blank for 97.0% of victims here, so victims who live elsewhere cannot be separated.
- Ages in the city file: The city's incident file has no victim age. In the Where section, ages come from the city's Police Person table, linked by incident, race, ethnicity and sex. 98.2% of women in simple assaults and 95.3% of women in aggravated assaults have a linked age; the rest drop out of the model only.
- Neighborhood is not neutral: Police division and tract poverty, income, unemployment and housing are shaped by segregation and disinvestment. 32.7% of Black women live in census tracts where 25% or more of residents are poor, against 24.6% of Hispanic women, 5.4% of White women and 9.0% of Asian women. In the city file's subset, tract socioeconomics narrow the gap from 2.8x to 2.18x. Where a control narrows a gap, the gap has been located, not explained away.
- Least stable comparison: The Asian comparison rests on 283 Asian women victims. Between the two sources and across years it moved up to 24%, against 14% or less for the others, so it is left out of the headline.
<!-- results:end -->

## How this differs from Los Angeles, DC and Baltimore

- **Source: the FBI's NIBRS files, as in DC.** Dallas police publish incident data with victim race on Dallas OpenData, but without family violence or any offense with a victim or suspect under 17. That leaves out most assaults on women (see the caveats). The FBI's NIBRS files for Texas hold every assault Dallas police reported, so the rates use them.
- **Partner assault, as in LA and DC.** NIBRS records each victim's relationship to the offenders, so the partner test runs. Baltimore could not run it.
- **Location from the city's own file.** NIBRS has no location. The city's file has coordinates and victim race, but only for non-family assaults on victims 17 and older. The division test and the tract model run on that subset (`city/analysis.json`), with victim ages linked from the city's Police Person table. The page labels it as that subset.
- **Ethnicity is a separate field, as in DC and Baltimore, but it is rarely missing.** A victim is Hispanic if the ethnicity field says so, whatever the race, and otherwise takes the recorded race. The bound on the Hispanic comparison is narrow.
- **Officers are left out, as in LA and DC.** NIBRS marks them as a victim type of their own.
- **Replication against the city's own file.** The FBI's file is filtered the way the city filters its own (no family or partner assault, no one under 17) and set against the city file for the same years.
- **Premises codes are unusual.** Dallas police file far more assaults under the FBI's commercial or office building category than other large Texas departments, most likely apartment complexes. The page labels it "Commercial/Office", not the kit's "Office Building", and the caveats give the numbers.

## Definitions

- Offenses: aggravated assault (13A, which includes non-fatal shootings) and simple assault (13B). Intimidation (13C, threats with no attack), homicide and sex offenses are left out.
- Agency: Dallas Police Department (ORI TXDPD0000). Other agencies in Dallas County are left out; the caveats count their victims.
- Victims: individuals of any age. Officers, businesses and society are other NIBRS victim types and are left out.
- Window: January 2022 to December 2025, all four full years in the FBI's files. The audit found no coverage breaks.
- Groups: Black, Hispanic, White and Asian, as recorded by officers. Hispanic of any race first, by the ethnicity field, otherwise the recorded race. Unknown race, sex, age and ethnicity stay unknown. Nothing is imputed.
- Partner: spouse, common-law spouse, boyfriend or girlfriend, ex-spouse, ex-boyfriend or girlfriend, same-sex relationship (NIBRS codes SE, CS, BG, XS, XR, HR).
- City-file subset: NIBRS codes 13A and 13B in the city file, person involvement "Victim", victim type "Individual", 2022 to 2025, police divisions as recorded (they match the 2022 division boundaries by location). Victim ages come from the Police Person table, linked by incident, race, ethnicity and sex; victims whose age cannot be linked drop out of the model only.

## Rebuild

Python from disparity-kit (`~/.claude/disparity-kit/.venv/bin/python`); `KIT=~/.claude/disparity-kit/kit`.

```bash
# data (raw files are not tracked: the city file is 1.3 GB)
python scripts/fetch_nibrs.py 2022 2023 2024 2025                       # -> data/raw/TX-<year>.zip
python $KIT/sources.py fetch https://www.dallasopendata.com/resource/qv6i-rri7 --out data/raw/dallas_incidents.csv
python $KIT/nibrs.py agencies data/raw/TX-*.zip
python $KIT/nibrs.py flatten data/raw/TX-*.zip --ori TXDPD0000 --ori TX0575300 --ori TX0570000 --ori TX0575400 --ori TX0572600 \
  --ori TX0575000 --ori TX057519E --ori TX0579000 --ori TX057529E --ori TX057829E --ori TX0573900 --ori TX0573800 --ori TX0574100 \
  --ori TX0573000 --ori TX057819E --out data/interim/victim_offenses.csv
python scripts/slim_inputs.py                                           # -> data/interim/victim_offenses_dpd.csv, dallas_incidents_slim.csv
python $KIT/audit.py data/interim/victim_offenses_dpd.csv --code offense_code --desc offense_name --id victim_id --date incident_date --out out/audit_nibrs.md
python $KIT/audit.py data/interim/dallas_incidents_slim.csv --code nibrs_code --desc nibrs_crime --id servnumid --date date1 --out out/audit_city.md
python $KIT/schema.py place "Dallas, TX" --out out/place.json

# NIBRS victims, one file per type, and the analysis
python $KIT/nibrs.py victims data/interim/victim_offenses.csv --ori TXDPD0000 --kind aggravated=13A --kind simple=13B \
  --race-rule hispanic-first --out-dir data --prefix dallas_
python scripts/premise_labels.py analysis.json
python $KIT/denominators.py analysis.json            # -> out/population.json
python $KIT/analyze.py analysis.json                 # -> out/results.json

# the city file: subset with locations, ages, division test and tract model
python $KIT/prepare.py data/interim/dallas_incidents_slim.csv --code nibrs_code --kind simple=13B --kind aggravated=13A \
  --keep involvement=Victim --keep victimtype=Individual --hispanic-first --race comprace --ethnicity compethnicity \
  --hispanic "Hispanic or Latino" --out-dir data/city --prefix dallas_city_
python scripts/city_ages.py                          # -> data/raw/dallas_person_victims.csv, data/city/*_aged.csv
python $KIT/schema.py districts data/city/dallas_city_aggravated_aged.csv --district division --lat lat --lon lon \
  --geojson "https://services1.arcgis.com/In9TiV3Fv4nmmrag/arcgis/rest/services/Division2022/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson" \
  --out city/out/districts.json
python $KIT/denominators.py city/analysis.json       # -> city/out/population.json
python $KIT/analyze.py city/analysis.json            # -> city/out/results.json

# replication, checks, page
python scripts/replication_counts.py analysis.json   # -> out/replication_counts.json, out/city_file_coverage.json
python $KIT/replicate.py analysis.json               # -> out/replication.json
python scripts/dallas_checks.py analysis.json        # -> out/dallas_checks.json; extra_caveats, headline, question in analysis.json
python scripts/page_extras.py analysis.json          # -> out/extra_sections.json
python $KIT/build_page.py analysis.json              # -> index.html, results block above
python $KIT/bias_scan.py analysis.json               # -> out/bias_review.md
```

## Files

- `data/raw/*.source.json`: where each raw file came from (url or key, time, rows or size and checksum). The raw files are refetched with the commands above.
- `data/dallas_simple.csv`, `data/dallas_aggravated.csv`: the analysis input, one row per NIBRS victim, Dallas Police Department, with `race_group`, `partner` and `premise_label`.
- `data/city/dallas_city_<kind>_aged.csv`: the city-file subset with linked ages. `data/city/prepare.json` records the split.
- `analysis.draft.json`: the config as `/new-city` drafted it, before the decisions. `analysis.json` is the one the kit runs. `city/analysis.json` runs the kit on the city-file subset.
- `scripts/`: the Dallas steps the kit does not cover (downloads, premise labels, age link, replication counts, checks, page sections).
- `out/`: the source inspections, audits, mapping, population, results, checks, replication and bias review. `city/out/`: the same for the subset.

## Sources

- FBI, [Crime Data Explorer](https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads), NIBRS incident data by state, Texas, 2022 to 2025.
- Dallas Police Department, [Police Incidents](https://www.dallasopendata.com/d/qv6i-rri7) and [Police Person](https://www.dallasopendata.com/d/chez-ydz4), Dallas OpenData.
- Dallas Police Department GIS, [police divisions, 2022](https://services1.arcgis.com/In9TiV3Fv4nmmrag/arcgis/rest/services/Division2022/FeatureServer/0).
- US Census Bureau, ACS 2020 to 2024 five-year estimates, via [Census Reporter](https://censusreporter.org/profiles/16000US4819000-dallas-tx/).
