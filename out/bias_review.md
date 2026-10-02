# Racial bias review

Focus: Black women. This screen finds candidates; read every flag in context before acting.

## Data

- **note: race coding.** Officers record race by sight; the denominator is Black alone. Alone or in combination is 7% larger. Worst-case ratios: Hispanic 2.11x (from 2.26x), White 3.64x (from 3.91x), Asian 12.6x (from 13.52x). The writeup must state this bound.
- **note: overlapping denominators.** Share of each race-alone group that is also Hispanic: {'Black': 1.3, 'Asian': 1.5}. These residents count in two denominators; small shares are tolerable, large ones need non-Hispanic tables.
- **note: race outside the groups.** 0.3% of victims map to no group. Largest raw codes: `P` 107, `I` 90, `U` 53. Check none of them should belong to a group.
- **note: unknown race by sex.** Women 0.2%, men 0.4%.
- **note: small groups.** Under 50,000 residents of the focus sex: Asian. Their rates carry more noise.
- **note: enforcement and reporting.** Police data reflects where police patrol and who calls them. Heavier policing or more reporting in some neighborhoods raises recorded rates there. The writeup must say the data cannot separate this from real differences.
- **note: controls are not neutral.** Neighborhood, income and housing are shaped by segregation and discrimination. A gap that shrinks after these controls has been located, not explained away; say so.

## Writeup

Files: `index.html`, `README.md`

### index.html
- **review: Causal claim** (`causes`): "The data says Black women are assaulted at a higher rate. It does not say why. Nothing here measures causes, offenders or circumstances."  
  The data shows rates, not causes. Keep causal words only in sentences that say a cause is not measured.
- **review: Causal claim** (`because`): "Aggravated (13A) and simple (13B) assault reported by the Dallas Police Department, individual victims of any age, 6,282 of them under 17. Non-fatal shootings are aggravated assaults in NIBRS and are included. Left out: ..."  
  The data shows rates, not causes. Keep causal words only in sentences that say a cause is not measured.
- **review: Offender implication** (`suspect`): "Dallas police publish incident data on Dallas OpenData with victim race and locations, but without family violence or any offense with a victim or suspect under 17. For 2022 to 2025 it holds 8,411 assaults on women in th..."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Offender implication** (`suspect`): "Dallas police publish their incidents with family violence, and offenses where a victim or suspect is under 17, removed. NIBRS 2022 to 2025 is filtered the same way here (women 17 or older, no partner or family relations..."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Offender implication** (`offenders`): "The data says Black women are assaulted at a higher rate. It does not say why. Nothing here measures causes, offenders or circumstances."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Offender implication** (`suspect`): "Dallas police publish their incident data without family violence or any offense with a victim or suspect under 17. The age rule is in the dataset's description. The family violence rule is not, but the file's family-vio..."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Offender implication** (`offender`): "Partner assaults are identified from the victim-offender relationship, which is unknown or blank for 13.6% of Black, 13.5% of Hispanic, 13.3% of White and 16.3% of Asian women victims. Partner assault is 37.5% of assault..."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Share-of-people claim** (`32.7% of Black women`): "32.7% of Black women live in census tracts where 25% or more of residents are poor, against 24.6% of Hispanic women, 5.4% of White women and 9.0% of Asian women. The tract model compares women in tracts with similar pove..."  
  Report rates count reports, not people. Do not convert them into shares of a population.
- **review: Share-of-people claim** (`1.3% of Black residents`): "1.3% of Black residents are also Hispanic, so they sit in both denominators."  
  Report rates count reports, not people. Do not convert them into shares of a population.
- **review: Share-of-people claim** (`32.7% of Black women`): "Police division and tract poverty, income, unemployment and housing are shaped by segregation and disinvestment. 32.7% of Black women live in census tracts where 25% or more of residents are poor, against 24.6% of Hispan..."  
  Report rates count reports, not people. Do not convert them into shares of a population.
- **review: Explained-away language** (`accounts for the gap`): "Women only (24,838 Black women, 25,223 other women). Each cut asks whether a plain explanation accounts for the gap."  
  Controls like neighborhood and income are themselves shaped by segregation and discrimination. 'Explained by location' does not mean 'not related to race'.
- **review: Explained-away language** (`explained away`): "Police division and tract poverty, income, unemployment and housing are shaped by segregation and disinvestment. 32.7% of Black women live in census tracts where 25% or more of residents are poor, against 24.6% of Hispan..."  
  Controls like neighborhood and income are themselves shaped by segregation and discrimination. 'Explained by location' does not mean 'not related to race'.

### README.md
- **FLAG: inconsistent capitalization.** Hispanic 30x vs hispanic 3x. Pick one style (AP capitalizes Black; be consistent for White).
- **review: Causal claim** (`causes`): "- This shows what, not why: The data says Black women are assaulted at a higher rate. It does not say why. Nothing here measures causes, offenders or circumstances."  
  The data shows rates, not causes. Keep causal words only in sentences that say a cause is not measured.
- **review: Causal claim** (`because`): "- What is counted: Aggravated (13A) and simple (13B) assault reported by the Dallas Police Department, individual victims of any age, 6,282 of them under 17. Non-fatal shootings are aggravated assaults in NIBRS and are i..."  
  The data shows rates, not causes. Keep causal words only in sentences that say a cause is not measured.
- **review: Offender implication** (`offenders`): "- This shows what, not why: The data says Black women are assaulted at a higher rate. It does not say why. Nothing here measures causes, offenders or circumstances."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Offender implication** (`suspect`): "- The city's public file leaves most assaults out: Dallas police publish their incident data without family violence or any offense with a victim or suspect under 17. The age rule is in the dataset's description. The fam..."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Offender implication** (`offender`): "- Intimate partner is a lower bound: Partner assaults are identified from the victim-offender relationship, which is unknown or blank for 13.6% of Black, 13.5% of Hispanic, 13.3% of White and 16.3% of Asian women victims..."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Offender implication** (`suspect`): "- **Source: the FBI's NIBRS files, as in DC.** Dallas police publish incident data with victim race on Dallas OpenData, but without family violence or any offense with a victim or suspect under 17. That leaves out most a..."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Offender implication** (`offenders`): "- **Partner assault, as in LA and DC.** NIBRS records each victim's relationship to the offenders, so the partner test runs. Baltimore could not run it."  
  Victim data says nothing about who offended. Remove, or state that offenders are not in the data.
- **review: Share-of-people claim** (`1.3% of Black residents`): "- Overlapping groups: 1.3% of Black residents are also Hispanic, so they sit in both denominators."  
  Report rates count reports, not people. Do not convert them into shares of a population.
- **review: Share-of-people claim** (`32.7% of Black women`): "- Neighborhood is not neutral: Police division and tract poverty, income, unemployment and housing are shaped by segregation and disinvestment. 32.7% of Black women live in census tracts where 25% or more of residents ar..."  
  Report rates count reports, not people. Do not convert them into shares of a population.
- **review: Explained-away language** (`explained away`): "- Neighborhood is not neutral: Police division and tract poverty, income, unemployment and housing are shaped by segregation and disinvestment. 32.7% of Black women live in census tracts where 25% or more of residents ar..."  
  Controls like neighborhood and income are themselves shaped by segregation and discrimination. 'Explained by location' does not mean 'not related to race'.

### Required statements

- present: says it does not explain why
- present: names reporting differences
- present: names the race-coding limit
- present: separates reports from people

## Reviewer questions (answer in prose, not by regex)

- Does any sentence invite the reader to infer who the offenders are?
- Would the framing read the same if the groups were swapped?
- Is the comparison group chosen to make the gap look larger (for example, headlining the most extreme pair)?
- Are structural explanations (segregation, policing intensity, access to services) acknowledged as unmeasured, without being asserted?
- Does the headline survive the race-coding worst case and the least favorable comparison?
- Is the focus group described with agency and dignity, as people harmed, not as a problem?