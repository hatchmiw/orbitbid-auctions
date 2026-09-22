#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import math
import re
import sys

THUMB_W = 360
THUMB_H = 270
LABEL_H = 44
COLS = 3
MARGIN = 18
BG = "white"

def fit_image(path: Path):
    im = Image.open(path).convert("RGB")
    im = ImageOps.exif_transpose(im)
    im.thumbnail((THUMB_W, THUMB_H), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (THUMB_W, THUMB_H), BG)
    x = (THUMB_W - im.width)//2
    y = (THUMB_H - im.height)//2
    canvas.paste(im, (x,y))
    return canvas

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: build_contact_sheets.py <auction_id>")
    auction_id=sys.argv[1]
    root=Path("auctions")/auction_id/"photos"
    if not root.exists():
        raise SystemExit(f"Missing {root}")

    def natural_key(path):
        return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\\d+)", path.name)]

    lot_dirs=sorted([p for p in root.iterdir() if p.is_dir()], key=natural_key)
    made=0
    for lotdir in lot_dirs:
        photos=sorted([p for p in lotdir.glob("*.jpg") if p.name not in ("contact.jpg", "review.jpg")])
        if not photos:
            continue
        rows=math.ceil(len(photos)/COLS)
        cell_w=THUMB_W
        cell_h=THUMB_H+LABEL_H
        sheet_w=MARGIN*2 + COLS*cell_w
        sheet_h=MARGIN*2 + rows*cell_h
        sheet=Image.new("RGB",(sheet_w,sheet_h),BG)
        draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(photos):
            row=i//COLS
            col=i%COLS
            x=MARGIN+col*cell_w
            y=MARGIN+row*cell_h
            tile=fit_image(p)
            sheet.paste(tile,(x,y))
            draw.rectangle((x,y+THUMB_H,x+cell_w-1,y+cell_h-1), fill=(245,245,245))
            draw.text((x+12,y+THUMB_H+10), f"Lot {lotdir.name} — Photo {i+1} ({p.name})", fill="black")
        out=lotdir/"review.jpg"
        sheet.save(out,"JPEG",quality=72,optimize=True,progressive=True)
        print(out)
        made+=1
    print(f"Created {made} contact sheets")

if __name__=="__main__":
    main()
