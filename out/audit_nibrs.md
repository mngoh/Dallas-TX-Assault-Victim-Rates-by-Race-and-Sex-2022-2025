# Audit: data/interim/victim_offenses_dpd.csv

424,208 rows, 24 columns. Guessed: date `incident_date`, code `offense_code`, description `offense_name`, id `victim_id`. Override with flags if wrong.

## Missing and coded-missing values

| column | blank | coded missing (0, X, UNKNOWN...) | distinct |
|---|---|---|---|
| file_year | 0.0% | 0.0% | 4 |
| agency | 0.0% | 0.0% | 1 |
| ori | 0.0% | 0.0% | 1 |
| incident_id | 0.0% | 0.0% | 373,957 |
| incident_date | 0.0% | 0.0% | 1,461 |
| report_date_flag | 0.0% | 0.0% | 2 |
| incident_hour | 0.0% | 6.5% | 24 |
| offense_id | 0.0% | 0.0% | 399,657 |
| offense_code | 0.0% | 0.0% | 50 |
| offense_name | 0.0% | 0.0% | 51 |
| attempt_complete | 0.0% | 0.0% | 2 |
| location | 0.0% | 0.0% | 46 |
| victim_id | 0.0% | 0.0% | 407,531 |
| victim_seq_num | 0.0% | 0.0% | 39 |
| victim_type | 0.0% | 0.0% | 7 |
| age_code | 0.0% | 0.0% | 101 |
| age_num | 0.0% | 0.0% | 101 |
| sex | 0.0% | 26.3% | 4 |
| race | 0.0% | 0.7% | 7 |
| ethnicity | 0.0% | 27.9% | 4 |
| resident_status | 98.6% | 0.1% | 3 |
| relationship | 73.7% | 0.0% | 188 |
| weapon | 74.1% | 0.2% | 96 |
| injury | 87.4% | 0.0% | 57 |

## Duplicates

16,677 rows share an id in `victim_id`. One row per victim or offense? Decide before counting.

## Every offense value

Read the whole list. Related offenses are often coded separately (intimate partner, on police, on children, attempts).

| offense_code | offense_name | rows |
|---|---|---|
| 13B | Simple Assault | 60,099 |
| 240 | Motor Vehicle Theft | 57,986 |
| 23F | Theft From Motor Vehicle | 49,604 |
| 290 | Destruction/Damage/Vandalism of Property | 38,588 |
| 35A | Drug/Narcotic Violations | 35,066 |
| 23H | All Other Larceny | 29,587 |
| 220 | Burglary/Breaking & Entering | 25,664 |
| 13A | Aggravated Assault | 24,452 |
| 23G | Theft of Motor Vehicle Parts or Accessories | 16,831 |
| 13C | Intimidation | 16,568 |
| 23C | Shoplifting | 13,278 |
| 120 | Robbery | 11,346 |
| 520 | Weapon Law Violations | 9,074 |
| 26A | False Pretenses/Swindle/Confidence Game | 7,927 |
| 35B | Drug Equipment Violations | 6,308 |
| 23D | Theft From Building | 3,726 |
| 280 | Stolen Property Offenses | 3,286 |
| 26F | Identity Theft | 2,053 |
| 11A | Rape | 1,299 |
| 26B | Credit Card/Automated Teller Machine Fraud | 1,207 |
| 270 | Embezzlement | 1,117 |
| 250 | Counterfeiting/Forgery | 937 |
| 11D | Criminal Sexual Contact | 855 |
| 40A | Prostitution | 837 |
| 09A | Murder and Nonnegligent Manslaughter | 718 |
| 100 | Kidnapping/Abduction | 713 |
| 200 | Arson | 659 |
| 720 | Animal Cruelty | 510 |
| 23A | Pocket-picking | 446 |
| 11B | Sodomy | 441 |
| 40C | Purchasing Prostitution | 430 |
| 370 | Pornography/Obscene Material | 315 |
| 39A | Betting/Wagering | 299 |
| 11D | Fondling | 272 |
| 11C | Sexual Assault With An Object | 250 |
| 40B | Assisting or Promoting Prostitution | 247 |
| 26E | Wire Fraud | 241 |
| 64A | Human Trafficking, Commercial Sex Acts | 190 |
| 210 | Extortion/Blackmail | 152 |
| 23B | Purse-snatching | 128 |
| 09B | Negligent Manslaughter | 104 |
| 26C | Impersonation | 100 |
| 23E | Theft From Coin-Operated Machine or Device | 90 |
| 09C | Justifiable Homicide | 82 |
| 26G | Hacking/Computer Invasion | 54 |
| 26D | Welfare Fraud | 34 |
| 64B | Human Trafficking, Involuntary Servitude | 13 |
| 510 | Bribery | 11 |
| 36A | Incest | 8 |
| 39B | Operating/Promoting/Assisting Gambling | 5 |
| 39C | Gambling Equipment Violation | 1 |

## Coverage by month

0 unparseable dates. Range 2022-01-01 to 2025-12-31.

Median 8,978 rows a month. Months under 60% of that (system changes, partial periods, reporting lag):

- none

Full series:

2022-01:9287 2022-02:7862 2022-03:9250 2022-04:9351 2022-05:10306 2022-06:9523 2022-07:9858 2022-08:9662 2022-09:9291 2022-10:9289 2022-11:8103 2022-12:8678 2023-01:8920 2023-02:8211 2023-03:9537 2023-04:9535 2023-05:9444 2023-06:9716 2023-07:10666 2023-08:9860 2023-09:9998 2023-10:9767 2023-11:9171 2023-12:9440 2024-01:9046 2024-02:8563 2024-03:9235 2024-04:9007 2024-05:9240 2024-06:9118 2024-07:8950 2024-08:8566 2024-09:7956 2024-10:8235 2024-11:7743 2024-12:7811 2025-01:7509 2025-02:7088 2025-03:7889 2025-04:7800 2025-05:8273 2025-06:8037 2025-07:8489 2025-08:8767 2025-09:8010 2025-10:8215 2025-11:7888 2025-12:8048

Use only full calendar years where you can; weight any partial year by its share of the year.