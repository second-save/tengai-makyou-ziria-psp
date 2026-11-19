"""Build build/NPJJ30029/CONTENT.DAT from the original one.

    build.py              patched build (applies every step in PATCHES)
    build.py --identity   no patches: asserts the output is byte-identical to the original
    build.py --poke       test build: one changed byte in the IPL title of track 02 (loader integrity test)

Chain: CONTENT.DAT -xor-> archive -> HCD9005_02.bin -zlib chunks-> PC Engine CD data track (2048-byte sectors).
The PSP ISO itself is not rebuilt: the game data lives in CONTENT.DAT on the memory stick."""
import hashlib, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import content_xor, hcd, vpce  # noqa: E402

ORIG_DIR = os.path.join(ROOT, 'rom', 'NPJJ30029')
OUT_DIR = os.path.join(ROOT, 'build', 'NPJJ30029')
TRACKS = ('HCD9005_02.bin', 'HCD9005_06.bin')   # track 06 is a near copy of 02 (data repeated after the audio)

EN_TRACK = os.path.join(ROOT, 'work', 'tenmatools', 'tenma', 'tenma_02_build.iso')   # made by tools/build_en.sh


def english_track(name, data):
    """Track 02 becomes the translated track from the tenmatools build. Track 06 stays, as in LIPEMCO's patch."""
    if name == TRACKS[0]:
        new = open(EN_TRACK, 'rb').read()
        assert len(new) == len(data), 'translated track has another size: %d != %d' % (len(new), len(data))
        data[:] = new


PATCHES = [english_track]   # functions (track_name, bytearray of the unpacked track) -> None, applied in order


def load_tracks(plain):
    ents = {n: (o, s) for n, o, s in vpce.entries(plain)}
    return {t: plain[ents[t][0]:ents[t][0] + ents[t][1]] for t in TRACKS}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    enc = open(os.path.join(ORIG_DIR, 'CONTENT.DAT'), 'rb').read()
    key = content_xor.find_key(enc)
    plain = b''.join(content_xor.xor(enc[o:o + (1 << 22)], key) for o in range(0, len(enc), 1 << 22))
    repl = {}
    if mode != '--identity':
        for name, packed in load_tracks(plain).items():
            data = bytearray(hcd.unpack(packed))
            before = bytes(data)
            if mode == '--poke':
                if name == TRACKS[0]:
                    # the IPL's program name; not the "PC Engine CD-ROM SYSTEM" string before it, which the
                    # System Card checks (changing that hangs the boot at JUST A MOMENT)
                    i = data.index(b'TENGAIMAKYOU    ZIRIA ')
                    data[i + 21] = ord('!')
            else:
                for p in PATCHES:
                    p(name, data)
            if bytes(data) != before:
                assert len(data) == len(before), 'track size must not change (the .hcd sheet holds its length)'
                repl[name] = hcd.pack(bytes(data), packed)
    new_plain = vpce.pack(plain, repl)
    out = b''.join(content_xor.xor(new_plain[o:o + (1 << 22)], key) for o in range(0, len(new_plain), 1 << 22))
    if mode == '--identity':
        assert out == enc, 'identity build differs from the original'
        print('identity OK')
        return
    os.makedirs(OUT_DIR, exist_ok=True)
    open(os.path.join(OUT_DIR, 'CONTENT.DAT'), 'wb').write(out)
    shutil.copy(os.path.join(ORIG_DIR, 'psp-key.edat'), OUT_DIR)
    print('built %s  sha1 %s  replaced %s' % (OUT_DIR, hashlib.sha1(out).hexdigest(), sorted(repl) or 'nothing'))


if __name__ == '__main__':
    main()
