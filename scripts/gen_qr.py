"""Regenerate the QR code once the real domain is live.

Usage:
    python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
    .venv/bin/python scripts/gen_qr.py https://dagandgayle.com
"""
import sys
import re
import qrcode
import qrcode.image.svg
from qrcode.constants import ERROR_CORRECT_H

ROOT = __file__.rsplit("/scripts/", 1)[0]
FILL = "#14161A"
BACK = "#FFFFFF"


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "https://dagandgayle.com"

    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H, box_size=20, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=FILL, back_color=BACK).convert("RGB")
    img.save(f"{ROOT}/pictures/qr-code.png")

    qr_svg = qrcode.QRCode(
        version=None, error_correction=ERROR_CORRECT_H, box_size=20, border=2,
        image_factory=qrcode.image.svg.SvgPathImage,
    )
    qr_svg.add_data(url)
    qr_svg.make(fit=True)
    img_svg = qr_svg.make_image(fill_color=FILL, back_color=BACK)
    svg_path = f"{ROOT}/pictures/qr-code.svg"
    img_svg.save(svg_path)

    # qrcode's SvgPathImage doesn't draw a background rect or apply fill_color
    # to the path itself — patch both in, and make sure there's exactly one
    # `fill` attribute on the <path> (a duplicate makes it invalid XML and
    # browsers will silently refuse to render it as an <img>).
    with open(svg_path) as f:
        svg = f.read()
    svg = re.sub(r"(<svg[^>]*>)", rf'\1<rect width="100%" height="100%" fill="{BACK}"/>', svg, count=1)
    svg = re.sub(r'fill="#000000"', f'fill="{FILL}"', svg, count=1)
    with open(svg_path, "w") as f:
        f.write(svg)

    print(f"Regenerated pictures/qr-code.png and qr-code.svg for {url}")


if __name__ == "__main__":
    main()
