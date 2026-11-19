"""Test: is CONTENT.DAT a repeating-key XOR? Take the most repeated run as keystream candidate and try every phase.
usage: probe_xor.py CONTENT.DAT"""
import collections, sys

d = open(sys.argv[1], 'rb').read()
# period of the repeated region: distance between two occurrences of the same 16-byte block
blocks = collections.defaultdict(list)
for i in range(0x7000000, len(d) - 15, 16):
    blocks[d[i:i + 16]].append(i)
top = max(blocks.values(), key=len)
gaps = collections.Counter(b - a for a, b in zip(top, top[1:]))
print('most repeated block: %d times, gaps %s' % (len(top), gaps.most_common(4)))
period = gaps.most_common(1)[0][0]
start = top[0]
unit = d[start:start + period]
print('period 0x%X, sample start 0x%X, file offset mod period = 0x%X' % (period, start, start % period))
# does XOR with the unit (aligned to absolute file offset) give plain data elsewhere?
key = bytes(unit[(i - start) % period] for i in range(period))   # key[i] applies to file offset i mod period
for off in (0, 0x10, 0x800, 0x100000, 0x3000000):
    p = bytes(d[off + i] ^ key[(off + i) % period] for i in range(64))
    print('%08X %s %r' % (off, p.hex(), p))
