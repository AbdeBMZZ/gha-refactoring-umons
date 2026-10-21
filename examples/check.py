#!/usr/bin/env python3
"""Sanity checks for the refactoring exemplars.

1. Every workflow / action file in examples/ is valid YAML.
2. R3 (YAML anchors), if present: after alias expansion, `after` equals `before`.
3. R4 (workflow template), if present: each instantiated workflow equals the
   template with `$default-branch` resolved to `main` (apart from the name).

Run:  python3 examples/check.py
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
errors = []


def load(p: Path):
    # PyYAML maps the key `on` to True (YAML 1.1); normalise it back.
    data = yaml.safe_load(p.read_text())
    if isinstance(data, dict) and True in data:
        data["on"] = data.pop(True)
    return data


files = sorted(p for p in ROOT.rglob("*") if p.suffix in {".yml", ".yaml"})
for f in files:
    try:
        load(f)
    except yaml.YAMLError as e:
        errors.append(f"{f.relative_to(ROOT)}: invalid YAML: {e}")
print(f"[1] parsed {len(files)} YAML files")

r3 = ROOT / "R3-introduce-yaml-anchors"
if (r3 / "before/.github/workflows/python-ci.yml").is_file():
    b = load(r3 / "before/.github/workflows/python-ci.yml")
    a = load(r3 / "after/.github/workflows/python-ci.yml")
    if a != b:
        errors.append("R3: expanded 'after' differs from 'before'")
    print("[2] R3 before == expanded after:", a == b)
else:
    print("[2] R3 not present, skipped")

r4 = ROOT / "R4-extract-workflow-template"
tpl_path = r4 / "after/org-dotgithub/workflow-templates/java-maven-ci.yml"
if tpl_path.is_file():
    tpl_text = tpl_path.read_text()
    tpl = yaml.safe_load(tpl_text.replace("$default-branch", "main"))
    tpl["on"] = tpl.pop(True)
    for repo in ("repo-a", "repo-b"):
        before = load(r4 / f"before/{repo}/.github/workflows/java-ci.yml")
        inst = load(r4 / f"after/{repo}/.github/workflows/java-ci.yml")
        for d in (before, inst):
            d.pop("name")
        t = dict(tpl)
        t.pop("name")
        ok = before == inst == t
        if not ok:
            errors.append(f"R4: {repo} instance differs from template/original")
        print(f"[3] R4 {repo} == template:", ok)
else:
    print("[3] R4 not present, skipped")

if errors:
    print("\nFAILED:\n  " + "\n  ".join(errors))
    sys.exit(1)
print("\nAll checks passed.")
