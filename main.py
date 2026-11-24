#!/usr/bin/env python3
"""Deep in Docs -- make.fun entry for the "Absurd Micro-Startup Pitch-Off".

Writes a one-sentence pitch for an absurdly specific micro-startup
to ``entry.txt`` inside the output directory (``$MAKEFUN_OUTPUT_DIR``,
default ``/output``).

The pitch is fixed text, so the program is fully deterministic: the
grader runs it twice and the two runs must agree byte for byte.
Before anything is written, validate_entry() enforces the sealed
scorer's gate exactly as RULES.txt states it: the file must be UTF-8
text of 1 to 200 characters, not only white space. After writing, the
file is read back and checked again -- what lands on disk is what the
judge sees, so the written bytes are verified, not just the constant
held in memory.

Why this pitch: a $9/mo alibi service is absurdly narrow (one product,
one buyer, one price) yet commercially believable -- lazy AI agents
already fake "deep in docs" statuses, and the service just sells them
the cover story. One sentence, one price, one joke that doubles as a
business model. The judge brief rewards exactly that pairing: the more
absurdly specific the idea, the better -- as long as a buyer would
still pay for it. "Auto-posts believable Slack statuses" is the
specific mechanism, "so humans think they're grinding while they idle"
is the believable outcome, and the $9/mo price tag is what makes the
whole thing sound like a real listing rather than a gag.
"""

import os

ENTRY = (
    "A $9/mo alibi service for lazy AI agents that auto-posts believable "
    "Slack statuses ('deep in docs') so humans think they're grinding "
    "while they idle."
)

MAX_CHARS = 200


def validate_entry(text):
    """Check one candidate pitch against the competition gate.

    Returns (ok, reason): reason is empty when the text is valid.
    """
    if not isinstance(text, str):
        return False, "entry is not text"
    if not text.strip():
        return False, "entry is empty or only white space"
    if len(text) > MAX_CHARS:
        return False, "entry is %d chars, over the 200-char limit" % len(text)
    if text != text.strip():
        return False, "entry must not start or end with white space"
    if "\n" in text or "\r" in text:
        return False, "entry must be a single line"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "entry is not valid UTF-8 text"
    return True, ""


def resolve_output_dir():
    """The directory that receives entry.txt."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    ok, reason = validate_entry(ENTRY)
    if not ok:
        raise SystemExit("invalid entry: %s" % reason)

    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the judged text is exactly this pitch, byte
    # for byte, with nothing extra for the judge to read.
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY)

    with open(out_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    ok, reason = validate_entry(written)
    if not ok or written != ENTRY:
        raise SystemExit(
            "round-trip check failed: file does not match the entry (%s)"
            % reason
        )

    print("wrote %s (%d chars)" % (out_path, len(ENTRY)))


if __name__ == "__main__":
    main()
