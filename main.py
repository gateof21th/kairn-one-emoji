#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One Emoji, One Smile — entry program.

Writes exactly one emoji (the sun with face, U+1F31E) to the output
directory as entry.txt. The competition's sealed gate requires UTF-8
text of 1 to 8 characters, not only white space; this entry is a
single character.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMOJI_FILE = os.path.join(HERE, "emoji.txt")


def load_emoji() -> str:
    with open(EMOJI_FILE, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8")  # strict: raises on invalid UTF-8
    if not (1 <= len(text) <= 8):
        raise ValueError(f"entry must be 1-8 characters, got {len(text)}")
    if text.strip() == "":
        raise ValueError("entry must not be only white space")
    return text


def main() -> int:
    text = load_emoji()
    payload = text.encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # Atomic write: temp file in the same directory, then rename over
    # the target so a reader never sees a half-written entry.
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "wb") as fh:
        fh.write(payload)
    os.replace(tmp_path, out_path)
    # Round-trip verification: what landed on disk must be byte-exact.
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != payload:
        raise IOError("entry.txt on disk does not match the intended emoji")
    return 0


if __name__ == "__main__":
    sys.exit(main())
