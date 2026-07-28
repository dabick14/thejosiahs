"""Regenerate the downloadable invitation PDF — e.g. once the venue name,
domain, or wording is confirmed. Run gen_qr.py first if the domain changed,
since this embeds pictures/qr-code.png.

Usage:
    python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
    .venv/bin/python scripts/gen_invitation.py
"""
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/System/Library/Fonts/Supplemental"  # macOS Georgia — swap for any serif .ttf on other OSes
ROOT = __file__.rsplit("/scripts/", 1)[0]

GRAPHITE = (20, 22, 26)
BODY = (58, 61, 66)
MUTED = (138, 143, 152)
CHROME = (158, 163, 171)
BORDER = (223, 226, 230)
WHITE = (255, 255, 255)

# A5 @ 300dpi
W, H = 1748, 2480


def tracked_text(draw, xy, text, font, fill, tracking=0, anchor_center_x=None):
    if tracking == 0:
        if anchor_center_x is not None:
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            xy = (anchor_center_x - w / 2, xy[1])
        draw.text(xy, text, font=font, fill=fill)
        return
    x, y = xy
    widths = [draw.textbbox((0, 0), ch, font=font)[2] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    if anchor_center_x is not None:
        x = anchor_center_x - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    reg = ImageFont.truetype(f"{FONT_DIR}/Georgia.ttf", 34)
    reg_sm = ImageFont.truetype(f"{FONT_DIR}/Georgia.ttf", 28)
    ital = ImageFont.truetype(f"{FONT_DIR}/Georgia Italic.ttf", 30)
    names_font = ImageFont.truetype(f"{FONT_DIR}/Georgia.ttf", 96)
    label_font = ImageFont.truetype(f"{FONT_DIR}/Georgia.ttf", 22)

    margin = 90
    d.rectangle([margin, margin, W - margin, H - margin], outline=BORDER, width=2)
    d.rectangle([margin + 14, margin + 14, W - margin - 14, H - margin - 14], outline=BORDER, width=1)

    cx = W / 2
    y = 300

    tracked_text(d, (0, y), "TOGETHER WITH THEIR FAMILIES", label_font, MUTED, tracking=10, anchor_center_x=cx)
    y += 90
    tracked_text(d, (0, y), "Dag Josiah", names_font, GRAPHITE, anchor_center_x=cx)
    y += 118
    tracked_text(d, (0, y), "&", ital, CHROME, anchor_center_x=cx)
    y += 90
    tracked_text(d, (0, y), "Gayle Hughes", names_font, GRAPHITE, anchor_center_x=cx)
    y += 170

    r = 22
    d.ellipse([cx - r * 1.6, y, cx - r * 1.6 + r * 2, y + r * 2], outline=CHROME, width=3)
    d.ellipse([cx - r * 0.4, y + 8, cx - r * 0.4 + r * 2, y + 8 + r * 2], outline=CHROME, width=3)
    y += 110

    tracked_text(d, (0, y), "request the pleasure of your company", reg, BODY, anchor_center_x=cx)
    y += 52
    tracked_text(d, (0, y), "at their wedding", reg, BODY, anchor_center_x=cx)
    y += 110

    tracked_text(d, (0, y), "Saturday, the Eighth of August", ital, GRAPHITE, anchor_center_x=cx)
    y += 50
    tracked_text(d, (0, y), "Two Thousand and Twenty-Six", ital, GRAPHITE, anchor_center_x=cx)
    y += 96

    d.line([cx - 60, y, cx + 60, y], fill=BORDER, width=2)
    y += 60

    tracked_text(d, (0, y), "White Wedding Ceremony", reg, GRAPHITE, anchor_center_x=cx)
    y += 48
    tracked_text(d, (0, y), "Venue & time to be confirmed", reg_sm, MUTED, anchor_center_x=cx)
    y += 42
    tracked_text(d, (0, y), "— full details at dagandgayle.com", reg_sm, MUTED, anchor_center_x=cx)
    y += 130

    qr = Image.open(f"{ROOT}/pictures/qr-code.png").convert("RGB")
    qr_size = 300
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)
    img.paste(qr, (int(cx - qr_size / 2), int(y)))
    y += qr_size + 40

    tracked_text(d, (0, y), "SCAN FOR FULL DETAILS & RSVP", label_font, MUTED, tracking=8, anchor_center_x=cx)

    img.save(f"{ROOT}/dag-and-gayle-invitation.pdf", "PDF", resolution=300.0)
    img.save(f"{ROOT}/pictures/invitation-preview.webp", "WEBP", quality=80)
    print("Regenerated dag-and-gayle-invitation.pdf and pictures/invitation-preview.webp")


if __name__ == "__main__":
    main()
