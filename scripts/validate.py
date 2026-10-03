#!/usr/bin/env python3
"""Checks android.yaml: known fields only, unique ids, a source and triggers for every entry."""

import sys

import yaml

TRIGGERS = {"uses", "manifest", "qualifiers", "features"}
SHAPES = {"compact", "landscape", "foldable", "tablet"}
FIELDS = {
    "behavior": {"id", "api", "by", "both_sides", "summary", "verify", "source"} | TRIGGERS,
    "form_factors": {"id", "cells", "state", "needs", "summary", "verify", "source"} | TRIGGERS,
    "vendors": {"id", "vendors", "summary", "verify", "source"} | TRIGGERS,
}


def check(doc):
    errors = []
    if set(doc) != set(FIELDS):
        errors.append(f"top level must be exactly {sorted(FIELDS)}, is {sorted(doc)}")
        return errors
    ids = set()
    for section, allowed in FIELDS.items():
        for i, e in enumerate(doc[section]):
            where = f"{section}[{i}] {e.get('id', '?')}"
            unknown = set(e) - allowed
            if unknown:
                errors.append(f"{where}: unknown fields {sorted(unknown)}")
            for field in ("id", "summary", "verify", "source"):
                if not isinstance(e.get(field), str) or not e[field].strip():
                    errors.append(f"{where}: needs `{field}`")
            if e.get("id") in ids:
                errors.append(f"{where}: duplicate id")
            ids.add(e.get("id"))
            if not str(e.get("source", "")).startswith("https://"):
                errors.append(f"{where}: `source` must be an https link")
            if not any(e.get(t) for t in TRIGGERS):
                errors.append(f"{where}: needs a trigger ({', '.join(sorted(TRIGGERS))})")
            for t in TRIGGERS:
                v = e.get(t, [])
                if not isinstance(v, list) or not all(isinstance(x, str) and x for x in v):
                    errors.append(f"{where}: `{t}` must be a list of names")
            if section == "behavior":
                if not isinstance(e.get("api"), int) or not 1 <= e["api"] <= 99:
                    errors.append(f"{where}: `api` must be an API level")
                if e.get("by") not in ("device", "target"):
                    errors.append(f"{where}: `by` must be device or target")
            if section == "form_factors":
                cells, needs = e.get("cells"), e.get("needs")
                if bool(cells) == bool(needs):
                    errors.append(f"{where}: give `cells` or `needs`, not both or neither")
                if cells and not set(cells) <= SHAPES:
                    errors.append(f"{where}: cells must be among {sorted(SHAPES)}")
            if section == "vendors":
                vendors = e.get("vendors") or []
                if not vendors or any(v != v.lower() for v in vendors):
                    errors.append(f"{where}: `vendors` must be lowercase manufacturer names")
    return errors


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "android.yaml"
    with open(path, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    errors = check(doc)
    for e in errors:
        print(f"{path}: {e}")
    counts = {k: len(doc.get(k) or []) for k in FIELDS}
    if not errors:
        print(f"{path}: ok — {counts}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
