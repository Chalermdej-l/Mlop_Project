"""Helpers for maintaining KEY=value environment files."""

from __future__ import annotations

from pathlib import Path


def update_env_file(path: str | Path, key: str, value: str) -> None:
    """Set ``key=value`` in the file at ``path``.

    Replaces the line if the key already exists, otherwise appends it.
    Values are written unquoted to match the ``.env`` convention.
    """
    file_path = Path(path)
    lines = file_path.read_text().splitlines() if file_path.exists() else []

    replaced = False
    for index, line in enumerate(lines):
        if line.split("=", 1)[0].strip() == key:
            lines[index] = f"{key}={value}"
            replaced = True
            break
    if not replaced:
        lines.append(f"{key}={value}")

    file_path.write_text("\n".join(lines) + "\n")
