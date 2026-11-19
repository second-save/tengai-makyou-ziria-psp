"""Debug tool: read or change PSP memory inside a play.py savestate (headless PPSSPP fork, as tools/play.sh).

    poke.py dump STATE OUT.bin                 PSP user RAM 0x08800000..0x0A000000 (the PC Engine's RAM is in there)
    poke.py set STATE_IN STATE_OUT ADDR=HEXBYTES..   write bytes, run 2 frames, save the new state
                                               (ADDR as dump offset or 0x088.. address; 0x1234=0A00 writes 2 bytes)

Find an address with the skill's ramsearch.py over two dumps (--base 0x08800000). The memstick of the session
the state came from is passed with --memstick (default: work/play/en2/memstick)."""
import base64, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill import SKILL  # noqa: E402
sys.path.insert(0, os.path.join(SKILL, 'scripts'))
import glob  # noqa: E402
import psp  # noqa: E402

BASE, SIZE = 0x08800000, 0x01800000
EMU = os.environ.get('PPSSPP_HEADLESS') or os.path.expanduser(
    '~/develop/tengai-makyou-collection-psp/tools/ppsspp-headless/src/build/PPSSPPHeadless')


def main():
    a = sys.argv[1:]
    ms = os.path.join(ROOT, 'work', 'play', 'en2', 'memstick')
    if '--memstick' in a:
        i = a.index('--memstick'); ms = a[i + 1]; del a[i:i + 2]
    cmd, state = a[0], a[1]
    iso = glob.glob(os.path.join(ROOT, 'rom', '*.iso'))[0]
    run = psp.Run(EMU, iso, os.path.join(ROOT, 'work', 'poke'), state=state, memstick=os.path.abspath(ms))
    try:
        if cmd == 'dump':
            with open(a[2], 'wb') as f:
                for o in range(0, SIZE, 1 << 20):
                    f.write(run.ws.mem(BASE + o, 1 << 20))
        elif cmd == 'set':
            for kv in a[3:]:
                addr, hexs = kv.split('=')
                addr = int(addr, 16); addr += BASE if addr < BASE else 0
                data = bytes.fromhex(hexs)
                run.ws.call('memory.write', address=addr, base64=base64.b64encode(data).decode())
                assert run.ws.mem(addr, len(data)) == data, kv
            run.run_to(2)
            run.save_state(a[2])
        else:
            sys.exit(__doc__)
    finally:
        run.close()


main()
