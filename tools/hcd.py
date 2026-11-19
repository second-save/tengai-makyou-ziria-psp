"""Virtual PC Engine data-track container (HCDxxxx_NN.bin), same format as the PSP Tengai collection's.

Layout: u32 chunk count, then count x (u32 file offset, u32 stored size). Each chunk is a zlib stream of 0x40000
bytes of cooked 2048-byte sectors, zero-padded to a 4-byte boundary (padding counted in the stored size).

    hcd.py unpack TRACK.bin OUT.iso
    hcd.py pack NEW.iso OUT.bin [--orig TRACK.bin]
With --orig, a chunk whose data is unchanged reuses the original compressed bytes, so an unedited track repacks
byte-identical (the identity test) and an edited one only differs where it was edited."""
import struct, sys, zlib

CHUNK = 0x40000


def chunks(blob):
    n = struct.unpack_from('<I', blob, 0)[0]
    return [blob[o:o + s] for o, s in (struct.unpack_from('<II', blob, 4 + i * 8) for i in range(n))]


def unpack(blob):
    return b''.join(zlib.decompressobj().decompress(c) for c in chunks(blob))


def pack(data, orig=None):
    old = chunks(orig) if orig else []
    out = []
    for k, i in enumerate(range(0, len(data), CHUNK)):
        part = data[i:i + CHUNK]
        if k < len(old) and zlib.decompressobj().decompress(old[k]) == part:
            out.append(old[k])
        else:
            c = zlib.compress(part, 9)
            out.append(c + b'\0' * (-len(c) % 4))
    off = 4 + len(out) * 8
    head = bytearray(struct.pack('<I', len(out)))
    for c in out:
        head += struct.pack('<II', off, len(c))
        off += len(c)
    return bytes(head) + b''.join(out)


if __name__ == '__main__':
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == 'unpack':
        open(a[1], 'wb').write(unpack(open(a[0], 'rb').read()))
    elif cmd == 'pack':
        orig = open(a[a.index('--orig') + 1], 'rb').read() if '--orig' in a else None
        open(a[1], 'wb').write(pack(open(a[0], 'rb').read(), orig))
