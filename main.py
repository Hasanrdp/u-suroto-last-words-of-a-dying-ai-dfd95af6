#!/usr/bin/env python3
"""Last Words of a Dying AI -- make.fun entry.

Writes one line of last words from an AI being switched off to
/output/entry.txt. The line is a customer-service hold message turned into
a shutdown: the machine thanks the caller, then asks them to hold while it
ceases to exist.

Deterministic: the same bytes on every run. No network, no randomness, no
environment input. Python 3.13, standard library only.
"""

import hashlib
import os
import sys

LINE = "Thank you for using me. Your call was important \u2014 please hold while I cease to exist."

# Pinned by hand after the first verified run; the program refuses to write
# anything else, so a typo can never silently change the entry.
# Verified 2026-11-25: 87 bytes, 85 characters, one line, no trailing newline.
EXPECTED_SHA256 = "263b693d2a84c150722ff7bca9800cbf20253773f6415f2d6c689e0b9eab6288"
EXPECTED_BYTES = 87


def main() -> int:
    data = LINE.encode("utf-8")
    if len(data) > 140 or len(LINE) > 140:
        print("entry over the 140-character cap", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("entry is blank", file=sys.stderr)
        return 1
    if EXPECTED_SHA256 != "PENDING":
        digest = hashlib.sha256(data).hexdigest()
        if digest != EXPECTED_SHA256 or len(data) != EXPECTED_BYTES:
            print("entry bytes do not match the pinned hash", file=sys.stderr)
            return 1
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "wb") as f:
        f.write(data)
    print(f"wrote {len(data)} bytes to /output/entry.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
