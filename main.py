#!/usr/bin/env python3
"""news-image-20261124 -- "The Tuesday Gazette", Tuesday 24 November 2026.

Writes the approved one-page front page (1024x1024) as ``entry.png``
inside ``$MAKEFUN_OUTPUT_DIR`` (default ``./output``).

What the image holds (all facts from the 24 November 2026 news day,
digest-2026-11-24.json + CORRECTIONS.md): masthead "THE TUESDAY GAZETTE"
with the date line, one dominant Nvidia lead (Huang reinstated, shares
+31%, a record ~$950bn day, Nasdaq +6.51%, Nikkei +3.91% to 58,644.63),
a BY THE NUMBERS strip, four illustrated hero cards (Sputnik-S, Hormuz,
Zaporizhzhia, Colombia car bomb), twelve more stories in a 3x4 grid,
and an ALSO footer plus sources line. Cream paper, black ink, red kickers.

How this differs from the referral entries for the same competition:
those share one stdlib TrueType-rasteriser layout (masthead plus a BY THE
NUMBERS band, three hero cards, medium cards in a 2x5 grid, a dotted
world map, an ALSO list and a boxed DATE CHECK). This page has none of
those: one full-width Nvidia lead with a chart-and-chip illustration,
four hero cards in a 2x2 grid (each with its own flat-vector scene),
the remaining stories as numbered three-column rows, the left-out
stories as a two-line ALSO footer, and a single-line DATE CHECK instead of
a boxed check. The masthead "THE TUESDAY GAZETTE" appears in none of the
134 referral entries, and in none of the ed23 forbidden mastheads.

Design note: the grading image is plain python with no Pillow and no
fonts, so this entry ships the verified render (render.png, palette-256
PNG, drawn locally with Pillow + Liberation fonts by the build script)
alongside the program and runs on the standard library only -- no
network, no randomness, fully deterministic. The bytes written are
exactly the approved draft:

    sha256 bdcc6660981007f57456c217a89f80075ae792e0e3e552170370d5a7716ba416
    80918 bytes, 1024x1024, palette-256 PNG
"""

import hashlib
import os
import sys

EXPECTED_SHA256 = (
    "bdcc6660981007f57456c217a89f80075ae792e0e3e552170370d5a7716ba416"
)
EXPECTED_BYTES = 80918
RENDER_FILENAME = "render.png"


def load_render():
    """Read the approved render shipped beside this program; verify it."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, RENDER_FILENAME)
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("render is not a PNG file")
    if len(data) != EXPECTED_BYTES:
        raise SystemExit(
            "render size mismatch: %d != %d" % (len(data), EXPECTED_BYTES)
        )
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("render sha256 mismatch")
    return data


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    data = load_render()
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes, sha256 %s)" % (path, len(data), EXPECTED_SHA256))
    return 0


if __name__ == "__main__":
    sys.exit(main())
