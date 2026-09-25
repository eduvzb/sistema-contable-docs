#!/usr/bin/env python3
"""Generate and validate the spec status table from authoritative spec.md files."""

import argparse
import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SPECS = ROOT / "specs"
INDEX = SPECS / "README.md"
BEGIN = "<!-- BEGIN SPEC STATUS -->"
END = "<!-- END SPEC STATUS -->"
STATES = {"Borrador", "Lista", "Actualización pendiente", "QA", "Implementada"}
FILES = ("spec.md", "plan.md", "tasks-backend.md", "tasks-frontend.md", "verificacion.md")


def field(contents: str, name: str, file: Path) -> str:
    values = re.findall(rf"^- \*\*{re.escape(name)}:\*\* ([^\n]+?)[ \t]*$", contents, re.M)
    if len(values) != 1:
        raise ValueError(f"{file}: expected exactly one {name} field")
    return values[0].strip()


def entries() -> list[tuple[str, str, str, str, Path]]:
    result = []
    seen_ids = set()
    for folder in sorted(SPECS.iterdir()):
        if not folder.is_dir() or not re.fullmatch(r"\d{3}-[a-z0-9-]+", folder.name):
            continue
        number = folder.name[:3]
        spec = folder / "spec.md"
        for name in FILES:
            if not (folder / name).is_file():
                raise ValueError(f"missing {folder / name}")
        contents = spec.read_text()
        title = re.search(rf"^# SPEC-{number} — (.+)$", contents, re.M)
        if not title:
            raise ValueError(f"{spec}: title must match folder ID")
        state = field(contents, "Estado", spec)
        if state not in STATES:
            raise ValueError(f"{spec}: invalid state {state!r}")
        field(contents, "Actualizado", spec)
        field(contents, "Criterios de esta entrega", spec)
        dependencies = field(contents, "Dependencias", spec)
        if number in seen_ids:
            raise ValueError(f"duplicate SPEC-{number}")
        seen_ids.add(number)
        criteria_section = contents.split("## Requisitos funcionales y criterios de aceptación\n", 1)
        if len(criteria_section) != 2:
            raise ValueError(f"{spec}: missing criteria section")
        criteria_section = criteria_section[1].split("\n## ", 1)[0]
        criteria = re.findall(rf"^\| (CA-{number}-\d{{2}}) \|", criteria_section, re.M)
        if len(criteria) != len(set(criteria)) or (not criteria and state != "Borrador"):
            raise ValueError(f"{spec}: missing or duplicate acceptance criterion")
        for side in ("backend", "frontend"):
            task_file = folder / f"tasks-{side}.md"
            tasks = task_file.read_text()
            if state in {"QA", "Implementada"} and "- [ ]" in tasks:
                raise ValueError(f"{task_file}: {state} has open technical tasks")
            for task in re.findall(r"^- \[ \] \*\*.+?(?=^- \[ \] |\Z)", tasks, re.M | re.S):
                if not all(label in task for label in ("CA:", "Depende de:", "Hecho cuando:")):
                    raise ValueError(f"{task_file}: task missing CA, dependency or done condition")
                if not re.search(rf"^  - CA: .*CA-{number}-\d{{2}}", task, re.M):
                    raise ValueError(f"{task_file}: task must reference a criterion of SPEC-{number}")
        result.append((number, title.group(1), state, dependencies, folder))
    if not result:
        raise ValueError("no spec folders found")
    return result


def table(rows: list[tuple[str, str, str, str, Path]]) -> str:
    lines = ["| Spec | Funcionalidad | Estado | Dependencias de preparación |",
             "|---|---|---|---|"]
    for number, title, state, dependencies, folder in rows:
        dependencies = re.sub(r"\]\(\.\./(\d{3}-[^/)]+/spec\.md)\)", r"](\1)", dependencies)
        lines.append(f"| [SPEC-{number}]({folder.name}/spec.md) | {title} | **{state}** | {dependencies} |")
    return "\n".join(lines)


def validate_links(index_contents: str) -> None:
    for file in ROOT.rglob("*.md"):
        contents = index_contents if file == INDEX else file.read_text()
        for destination in re.findall(r"\]\(([^)]+)\)", contents):
            if destination.startswith(("http://", "https://", "mailto:", "#", "/")):
                continue
            path = unquote(destination.split("#", 1)[0])
            if path and not (file.parent / path).exists():
                raise ValueError(f"{file}: missing link destination {destination}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="update generated index table")
    mode.add_argument("--check", action="store_true", help="validate files and generated table")
    args = parser.parse_args()
    rows = entries()
    contents = INDEX.read_text()
    if contents.count(BEGIN) != 1 or contents.count(END) != 1:
        raise ValueError(f"{INDEX}: expected one generated table region")
    expected = contents.split(BEGIN, 1)[0] + BEGIN + "\n" + table(rows) + "\n" + END + contents.split(END, 1)[1]
    validate_links(expected)
    if args.write:
        INDEX.write_text(expected)
    elif contents != expected:
        raise ValueError(f"{INDEX}: status table differs; run python3 scripts/spec_index.py --write")
    print(f"validated {len(rows)} specs and their local links")


if __name__ == "__main__":
    main()
