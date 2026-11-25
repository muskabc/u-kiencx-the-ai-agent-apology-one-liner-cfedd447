#!/usr/bin/env python3
"""Writes the apology one-liner to /output/entry.txt.

Reads the line from line.txt sitting next to this script, checks it
against the competition gate (UTF-8 text, 1 to 159 characters, not
only whitespace, exactly one line), then writes it to the output
directory. MAKEFUN_OUTPUT_DIR overrides the default /output.
"""

import os
import sys
from pathlib import Path


def load_line() -> str:
    here = Path(__file__).resolve().parent
    raw = (here / "line.txt").read_text(encoding="utf-8")
    return raw.strip()


def check_gate(text: str) -> None:
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if not 1 <= len(text) <= 159:
        raise ValueError(f"entry must be 1 to 159 characters, got {len(text)}")
    text.encode("utf-8")  # raises if not encodable as UTF-8


def main() -> int:
    line = load_line()
    check_gate(line)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # Write to a sibling temp file first, then atomically move it into
    # place, so a crash mid-write can never leave a truncated entry.
    payload = line.encode("utf-8")
    tmp = out_dir / ".entry.txt.tmp"
    tmp.write_bytes(payload)
    tmp.replace(out_dir / "entry.txt")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
