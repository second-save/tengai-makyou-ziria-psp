"""PSP VRAM dump -> PNG (480x272, stride 512). Fallback for PPSSPP builds whose debugger screenshot fails.
usage: fb.py VRAM.bin OUT.png [OFFSET=0] [FMT=8888|565|5551|4444]"""
import sys
from PIL import Image

d = open(sys.argv[1], 'rb').read()
off = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0
fmt = sys.argv[4] if len(sys.argv) > 4 else '8888'
if fmt == '8888':
    im = Image.frombuffer('RGBA', (512, 272), d[off:off + 512 * 272 * 4], 'raw', 'RGBA', 0, 1).convert('RGB')
else:
    raw = {'565': 'BGR;16', '5551': 'BGR;15', '4444': 'RGBA;4B'}[fmt]
    im = Image.frombuffer('RGB', (512, 272), d[off:off + 512 * 272 * 2], 'raw', raw, 0, 1)
    if fmt in ('565', '5551'):   # PSP stores red in the low bits
        r, g, b = im.split(); im = Image.merge('RGB', (b, g, r))
im.crop((0, 0, 480, 272)).save(sys.argv[2])
