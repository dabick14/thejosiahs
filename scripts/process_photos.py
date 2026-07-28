"""Convert new source photos into the site's WebP srcset pairs.

Drop full-res JPGs/PNGs into pictures/_originals/, add an entry to `mapping`
below (source filename -> output slug), then run:

    python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
    .venv/bin/python scripts/process_photos.py

Strips EXIF (including GPS) and produces <slug>-lg.webp (1600px long edge)
and <slug>-sm.webp (800px long edge) for use in srcset.
"""
import os
from PIL import Image, ImageOps

ROOT = __file__.rsplit("/scripts/", 1)[0]
SRC = f"{ROOT}/pictures/_originals"
OUT = f"{ROOT}/pictures"

# source filename (in pictures/_originals/) -> output slug
mapping = {
    # "new-photo.jpg": "gallery-06",
}

LG_MAX_EDGE = 1600
SM_MAX_EDGE = 800


def process(src_name, slug):
    img = Image.open(os.path.join(SRC, src_name))
    img = ImageOps.exif_transpose(img)  # bake in rotation before stripping EXIF
    img = img.convert("RGB")

    for suffix, max_edge in (("lg", LG_MAX_EDGE), ("sm", SM_MAX_EDGE)):
        w, h = img.size
        long_edge = max(w, h)
        if long_edge > max_edge:
            scale = max_edge / long_edge
            out = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        else:
            out = img.copy()
        out_path = os.path.join(OUT, f"{slug}-{suffix}.webp")
        # no exif kwarg => metadata (incl. GPS) is stripped
        out.save(out_path, "WEBP", quality=72, method=6)
        print(out_path, out.size, f"{os.path.getsize(out_path) / 1024:.0f}KB")


if __name__ == "__main__":
    if not mapping:
        print("Nothing to do — add entries to `mapping` in this script first.")
    for src_name, slug in mapping.items():
        process(src_name, slug)
