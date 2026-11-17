#!/usr/bin/env python3
"""Knipt een product uit een productfoto (rembg), met de ORIGINELE pixels van het product en een schoon masker.
Het product zelf wordt nooit aangepast; alleen de achtergrond verdwijnt.

Installatie (eenmalig per run): pip install --break-system-packages -q "rembg[cpu]" scipy
Gebruik: python3 tools/v7/cutout.py <in.png/jpg> <uit.png> [x0 y0 x1 y1]   (optioneel: uitsnede vóór het knippen)
Controleer het resultaat altijd op een gekleurde achtergrond (randen, doorschijnende stukken).
"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from rembg import remove, new_session

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
if len(sys.argv) == 7:
    im = im.crop(tuple(int(v) for v in sys.argv[3:7]))
mask = np.array(remove(im, session=new_session("isnet-general-use")).convert("RGBA"))[..., 3] > 25
lab, n = ndimage.label(mask)
if n > 1:
    sizes = ndimage.sum(mask, lab, range(1, n + 1)); mask = lab == (np.argmax(sizes) + 1)
mask = ndimage.binary_fill_holes(mask)
out = im.convert("RGBA"); out.putalpha(Image.fromarray((mask * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.0)))
out = out.crop(out.getbbox()); out.save(dst); print("ok", dst, out.size)
