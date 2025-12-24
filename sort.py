import os
from datetime import datetime

from icalendar import Calendar


def sort_ics_file(input_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    with open(input_path, "rb") as f:
        cal = Calendar.from_ical(f.read())

    sortable_components = []
    for comp in cal.walk():
        if comp.name in ("VEVENT", "VTODO", "VJOURNAL"):
            dtstart = comp.get("DTSTART")
            if dtstart:
                start_dt = dtstart.dt
                if isinstance(start_dt, datetime):
                    sort_key = start_dt
                else:
                    sort_key = datetime(start_dt.year, start_dt.month, start_dt.day)
            else:
                sort_key = datetime.max
            sortable_components.append((sort_key, comp))

    sortable_components.sort(key=lambda x: x[0])

    for comp in list(cal.subcomponents):
        if comp.name in ("VEVENT", "VTODO", "VJOURNAL"):
            cal.subcomponents.remove(comp)

    for _, comp in sortable_components:
        cal.subcomponents.append(comp)

    base, ext = os.path.splitext(input_path)
    output_path = base + "_sort" + ext

    with open(output_path, "wb") as f:
        f.write(cal.to_ical())

    print(f"Done！New file: {output_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python sort.py <input.ics>")
    else:
        sort_ics_file(sys.argv[1])
