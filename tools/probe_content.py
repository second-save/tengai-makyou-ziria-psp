"""Recon on CONTENT.DAT: entropy per region, repeated 16-byte blocks (ECB / unencrypted padding signs), zlib headers.
usage: probe_content.py CONTENT.DAT"""
import collections, math, sys, zlib

d = open(sys.argv[1], 'rb').read()
print('size %d = 0x%X; mod 16 = %d, mod 2048 = %d, mod 2352 = %d' % (len(d), len(d), len(d) % 16, len(d) % 2048, len(d) % 2352))

def ent(b):
    c = collections.Counter(b)
    return -sum(n / len(b) * math.log2(n / len(b)) for n in c.values())

for off in list(range(0, len(d), len(d) // 16)) + [len(d) - 65536]:
    print('entropy @%08X: %.3f' % (off, ent(d[off:off + 65536])))
blocks = collections.Counter(d[i:i + 16] for i in range(0, len(d) - 15, 16))
rep = [(n, b) for b, n in blocks.items() if n > 3]
rep.sort(reverse=True)
print('16-byte blocks: %d total, %d distinct, %d repeated >3x' % (sum(blocks.values()), len(blocks), len(rep)))
for n, b in rep[:12]:
    print('  %6dx %s first at %08X' % (n, b.hex(), d.find(b)))
for sig in (b'\x78\x9c', b'\x78\xda', b'\x78\x01', b'OggS', b'RIFF', b'\x00PGD', b'PSPEDAT'):
    n = d.count(sig)
    print('%r: %d hits, first %s' % (sig, n, hex(d.find(sig)) if n else '-'))
print('head', d[:64].hex())
print('tail', d[-64:].hex())
