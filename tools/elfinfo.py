"""Loader ELF recon: segments, sections, PSP import stubs (library + NIDs), and file offsets of given strings.
usage: elfinfo.py ELF [STRING..]"""
import struct, sys
from elftools.elf.elffile import ELFFile

path = sys.argv[1]
data = open(path, 'rb').read()
elf = ELFFile(open(path, 'rb'))
print('entry %08X type %s' % (elf.header.e_entry, elf.header.e_type))
segs = []
for s in elf.iter_segments():
    h = s.header
    segs.append(h)
    print('seg %-10s off %06X vaddr %08X filesz %06X memsz %06X' % (h.p_type, h.p_offset, h.p_vaddr, h.p_filesz, h.p_memsz))
for s in elf.iter_sections():
    h = s.header
    print('sec %-22s off %06X addr %08X size %06X' % (s.name, h.sh_offset, h.sh_addr, h.sh_size))

def v2o(v):
    for h in segs:
        if h.p_type == 'PT_LOAD' and h.p_vaddr <= v < h.p_vaddr + h.p_filesz:
            return v - h.p_vaddr + h.p_offset

def cstr(v):
    o = v2o(v)
    return data[o:data.index(b'\0', o)].decode('ascii', 'replace')

stub = elf.get_section_by_name('.lib.stub')
if stub:
    b = stub.data()
    for i in range(0, len(b), 20):
        name, flags, sz, nvar, nfun, nids, funcs = struct.unpack_from('<IIBBHII', b, i)
        print('import %s' % cstr(name))
        for k in range(nfun):
            nid = struct.unpack_from('<I', data, v2o(nids) + 4 * k)[0]
            print('  %08X nid %08X' % (funcs + 8 * k, nid))
for s in sys.argv[2:]:
    o = -1
    while (o := data.find(s.encode(), o + 1)) >= 0:
        print('string %r at file %06X' % (s, o))
