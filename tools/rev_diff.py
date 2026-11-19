"""How far is our disc from the Redump Revision 7 that tenmatools targets? Compares each tenma/base/NAME_SECTOR.bin
(Rev 7 code blocks) with our track at the same sector, using difflib opcodes on the bytes.
usage: rev_diff.py TRACK.iso TENMA_BASE_DIR"""
import difflib, os, re, sys

track = open(sys.argv[1], 'rb').read()
for f in sorted(os.listdir(sys.argv[2])):
    m = re.match(r'.*_([0-9A-F]+)\.bin$', f)
    if not m: continue
    a = open(os.path.join(sys.argv[2], f), 'rb').read()
    sec = int(m.group(1), 16)
    b = track[sec * 2048:sec * 2048 + len(a)]
    if a == b:
        print('%-22s sector %3X size %6X identical' % (f, sec, len(a))); continue
    same_pos = sum(x == y for x, y in zip(a, b))
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
    ins = sum(o[4] - o[3] for o in ops); dele = sum(o[2] - o[1] for o in ops)
    print('%-22s sector %3X size %6X same-position %5.1f%%  %d edits (-%d +%d bytes), first at %X'
          % (f, sec, len(a), 100 * same_pos / len(a), len(ops), dele, ins, ops[0][1]))
