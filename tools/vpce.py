"""Virtual PC Engine (PSN) CONTENT archive, after content_xor.py.
Layout: 0x80-byte header (magic 12 34 56 78, entry count u32 at 0x28, the rest unknown and kept as is), then
0x50-byte entries (name[0x40], offset u32, size u32, 8 zero bytes), then file data at 16-byte alignment.

    vpce.py list ARCHIVE
    vpce.py x ARCHIVE OUTDIR
    vpce.py pack ARCHIVE OUTFILE NAME=PATH..    replace files; everything else is copied unchanged
With no replacements, pack is byte-identical to ARCHIVE (the identity test)."""
import os, struct, sys

HDR, ENT = 0x80, 0x50


def entries(d):
    assert d[:4] == b'\x12\x34\x56\x78', 'not a plain VPCE archive (run content_xor.py first)'
    n = struct.unpack_from('<I', d, 0x28)[0]
    out = []
    for i in range(n):
        o = HDR + i * ENT
        name = d[o:o + 0x40].split(b'\0')[0].decode('ascii')
        off, size = struct.unpack_from('<II', d, o + 0x40)
        out.append((name, off, size))
    return out


def pack(d, repl):
    ents = entries(d)
    unknown = set(repl) - {n for n, _, _ in ents}
    assert not unknown, 'not in archive: %s' % unknown
    out = bytearray(d[:HDR + len(ents) * ENT])
    order = sorted(range(len(ents)), key=lambda i: ents[i][1])
    pos = ents[order[0]][1]
    assert pos == len(out)
    for k, i in enumerate(order):
        name, off, size = ents[i]
        # keep every file at its original offset modulo 512 (the XOR key period): files after a resized one then
        # keep their encrypted bytes, so an xdelta patch only carries the changed file
        out += b'\0' * ((off - pos) % 512)
        pos = len(out)
        end = ents[order[k + 1]][1] if k + 1 < len(order) else len(d)
        body = repl.get(name)
        if body is None:
            body, pad = d[off:off + size], d[off + size:end]     # original padding bytes, whatever they are
        else:
            pad = b'\0' * (-len(body) % 16)
        struct.pack_into('<II', out, HDR + i * ENT + 0x40, pos, len(body))
        out += body + pad
        pos = len(out)
    return bytes(out)


if __name__ == '__main__':
    cmd, arc = sys.argv[1], sys.argv[2]
    d = open(arc, 'rb').read()
    if cmd == 'list':
        for name, off, size in entries(d):
            print('%08X %9d %s' % (off, size, name))
        print('header', d[:HDR].hex())
    elif cmd == 'x':
        os.makedirs(sys.argv[3], exist_ok=True)
        for name, off, size in entries(d):
            open(os.path.join(sys.argv[3], name), 'wb').write(d[off:off + size])
    elif cmd == 'pack':
        repl = {}
        for a in sys.argv[4:]:
            n, p = a.split('=', 1)
            repl[n] = open(p, 'rb').read()
        open(sys.argv[3], 'wb').write(pack(d, repl))
