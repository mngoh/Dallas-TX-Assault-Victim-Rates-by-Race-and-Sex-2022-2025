"""Label one premises category the way the FBI names it.

Dallas police file far more assaults under NIBRS's "Commercial/Office Building" than other large Texas departments
(out/dallas_checks.json, "premises"), most likely apartment complexes: the city's own records list "Apartment
Complex/Building" as a premise, and NIBRS has no such category. The kit shortens "Commercial/Office Building" to
"Office Building" for chart axes, which would read as offices. Here it is "Commercial/Office", and the caveat
says what it probably holds. Every other label is the kit's.

Adds premise_label to each victim file; analysis.json reads it as the premise column. Run after nibrs.py victims.

  python scripts/premise_labels.py analysis.json
"""
import json
import pathlib
import sys

import pandas as pd

RELABEL = {"Office Building": "Commercial/Office"}


def main():
    cfg_path = pathlib.Path(sys.argv[1]).resolve()
    cfg = json.loads(cfg_path.read_text())
    for s in cfg["incidents"]:
        f = cfg_path.parent / s["path"]
        d = pd.read_csv(f, dtype=str, keep_default_na=False)
        d["premise_label"] = d["premise"].replace(RELABEL)
        d.to_csv(f, index=False)
        print(f"{f.name}: {int((d['premise'] != d['premise_label']).sum()):,} relabeled")


if __name__ == "__main__":
    main()
