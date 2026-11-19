"""CONTENT.DAT <-> plain archive. The file is XORed with a 512-byte key repeating from file offset 0 (XOR is its own
inverse, so the same command encrypts). The key is recovered from the file itself: the most repeated 512-byte unit is
0xFF padding. Pass --key FILE to use a saved key (needed once the padding has changed).
usage: content_xor.py IN OUT [--key KEYFILE] [--save-key KEYFILE]"""
import collections, sys

PERIOD = 512


def find_key(d):
    units = collections.Counter(d[i:i + PERIOD] for i in range(len(d) // 2 // PERIOD * PERIOD, len(d) - PERIOD, PERIOD))
    unit, n = units.most_common(1)[0]
    assert n > 100, 'no repeated padding unit found: pass --key'
    return bytes(b ^ 0xFF for b in unit)


def xor(d, key):
    k = int.from_bytes(key * (len(d) // PERIOD + 1), 'little') & ((1 << (8 * len(d))) - 1)
    return (int.from_bytes(d, 'little') ^ k).to_bytes(len(d), 'little')


if __name__ == '__main__':
    a = sys.argv[1:]
    d = open(a[0], 'rb').read()
    key = open(a[a.index('--key') + 1], 'rb').read() if '--key' in a else find_key(d)
    assert len(key) == PERIOD
    if '--save-key' in a: open(a[a.index('--save-key') + 1], 'wb').write(key)
    out = bytearray()
    for o in range(0, len(d), 1 << 22):   # 4 MB slices keep the big-int XOR fast
        out += xor(d[o:o + (1 << 22)], key)
    open(a[1], 'wb').write(out)
    print('wrote %s (%d bytes)' % (a[1], len(out)))
