"""The PSP side in English: the emulator's prompts and menus (EBOOT strings), the XMB title and picture, the
save title.

    frontend.py      -> build/ziria_en.iso (the user's ISO with the patched files swapped in)

The EBOOT is encrypted; the source is PPSSPP's decrypted dump (`DumpFileTypes = 7` in the emulator's ini, then
boot the game once): work/pphome/.config/ppsspp/PSP/SYSTEM/DUMP/NPJJ30029_EBOOT.BIN, sha1 checked below.
Strings are replaced in place from script/eboot.csv (offset, jp, en; "\\n" is the game's CR LF)."""
import csv, glob, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from skill import SKILL  # noqa: E402
sys.path.insert(0, os.path.join(SKILL, 'scripts'))
import iso9660, sfo  # noqa: E402
import io  # noqa: E402
from PIL import Image  # noqa: E402
from manual import C, T, V, render  # noqa: E402

ELF = os.path.join(ROOT, 'work', 'pphome', '.config', 'ppsspp', 'PSP', 'SYSTEM', 'DUMP', 'NPJJ30029_EBOOT.BIN')
ELF_SHA1 = 'bd7f46861b321f2f20f74a293076482268fea0e2'
ISO_SHA1 = 'a7ae6b1bb260264a03b7798ac4fad77fc51c778e'
TITLE = 'Tengai Makyo ZIRIA'
OUT = os.path.join(ROOT, 'build', 'ziria_en.iso')


def patch_eboot(elf):
    b = bytearray(elf)
    with open(os.path.join(ROOT, 'script', 'eboot.csv'), encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            off = int(row['offset'], 16)
            jp, en = (row[k].replace('\\n', '\r\n').encode('utf-8') for k in ('jp', 'en'))
            slot = (len(jp) + 4) & ~3   # string + NUL, padded to the next word
            assert off % 4 == 0 and b[off:off + slot] == jp.ljust(slot, b'\0'), row['offset'] + ': original differs'
            assert len(en) < slot, '%s: %d bytes, slot %d' % (row['offset'], len(en), slot)
            assert en.count(b'%') == jp.count(b'%'), row['offset'] + ': format codes differ'
            b[off:off + slot] = en.ljust(slot, b'\0')
    return bytes(b)


def iso_file(f, want):
    for path, lba, size, _ in iso9660.listing(f):
        if path == want:
            f.seek(lba * 2048)
            return f.read(size)
    raise KeyError(want)


SHADOW = (150, 150, 150)
PIC0 = [V(60, 20, 228, 50), T(66, 37, TITLE, 18, True, SHADOW), T(64, 35, TITLE, 18, True, (0, 0, 0)),
        V(18, 67, 293, 104)] + [s for i, line in enumerate((
            'This title can be played on PSP® and PS3®.',
            'For how to download it to PSP® and PS3® and more,',
            'see the official PlayStation®Network website.'))
            for s in (T(26, 75 + 12 * i, line, 9, True, SHADOW), T(25, 74 + 12 * i, line, 9, True, (0, 0, 0)))]


def pic0(png):
    """The XMB picture: title and notice in English; the alpha channel (rounded corners) is kept."""
    im = Image.open(io.BytesIO(png))
    new = render(im.convert('RGB'), PIC0).convert('RGBA')
    new.putalpha(im.getchannel('A'))
    b = io.BytesIO(); new.save(b, 'PNG', optimize=True)
    return b.getvalue()


def main():
    elf = open(ELF, 'rb').read()
    assert hashlib.sha1(elf).hexdigest() == ELF_SHA1, 'not the expected EBOOT dump (see this file\'s docstring)'
    src = glob.glob(os.path.join(ROOT, 'rom', '*.iso'))[0]
    h = hashlib.sha1()
    with open(src, 'rb') as f:
        for block in iter(lambda: f.read(1 << 24), b''): h.update(block)
    assert h.hexdigest() == ISO_SHA1, 'wrong base ISO: ' + h.hexdigest()
    boot = patch_eboot(elf)
    with open(src, 'rb') as f:
        param = sfo.set_str(iso_file(f, '/PSP_GAME/PARAM.SFO'), 'TITLE', TITLE)
        config = iso_file(f, '/PSP_GAME/USRDIR/CONFIG.PSP')
        pic = pic0(iso_file(f, '/PSP_GAME/PIC0.PNG'))
    old = 'SYS_TITLE_JP="天外魔境 ZIRIA"'.encode()   # the save data title
    assert config.count(old) == 1
    config = config.replace(old, ('SYS_TITLE_JP="%s"' % TITLE).encode())
    # shortcut: EBOOT.BIN is the plain patched ELF (PPSSPP only); sign it (sign_np -elf) before a PSP/Vita release
    repl = {'/PSP_GAME/SYSDIR/BOOT.BIN': boot, '/PSP_GAME/SYSDIR/EBOOT.BIN': boot, '/PSP_GAME/PARAM.SFO': param,
            '/PSP_GAME/USRDIR/CONFIG.PSP': config, '/PSP_GAME/PIC0.PNG': pic}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    iso9660.patch(src, OUT, repl)
    print('built %s' % OUT)


if __name__ == '__main__':
    main()
