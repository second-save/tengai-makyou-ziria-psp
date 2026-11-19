"""Rebuild a Redump Revision 7 data track from this disc's track: write tenmatools' base/NAME_SECTOR.bin code blocks
(original Rev 7 code, shipped with the LIPEMCO source) over the same sectors. Everything else is kept.
Also reports how many of tenmatools' raw resources (dumped from a real Rev 7 disc) occur in our track, as evidence
that the data outside the code blocks is the same in both revisions.
usage: make_rev7.py OUR_TRACK.iso TENMA_DIR OUT.iso"""
import os, re, sys

track = bytearray(open(sys.argv[1], 'rb').read())
tenma = sys.argv[2]
orig = bytes(track)
for f in sorted(os.listdir(os.path.join(tenma, 'base'))):
    m = re.match(r'.*_([0-9A-F]+)\.bin$', f)
    if not m: continue
    blk = open(os.path.join(tenma, 'base', f), 'rb').read()
    o = int(m.group(1), 16) * 2048
    track[o:o + len(blk)] = blk
open(sys.argv[3], 'wb').write(track)
print('wrote %s, %d bytes changed' % (sys.argv[3], sum(a != b for a, b in zip(orig, track))))

found = missing = 0
for root, _, files in os.walk(os.path.join(tenma, 'rsrc_raw')):
    for f in sorted(files):
        d = open(os.path.join(root, f), 'rb').read()
        if len(d) < 32: continue
        n = orig.count(d[:256])
        whole = orig.count(d) if n else 0
        found += bool(whole); missing += not whole
        if not whole:
            print('  not found whole: %s (%d bytes; first 256 bytes found %d times)' % (os.path.relpath(os.path.join(root, f), tenma), len(d), n))
print('rsrc_raw files found whole in our track: %d, not found: %d' % (found, missing))
