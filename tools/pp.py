"""Drive the stock PPSSPP SDL build on macOS (the skill's PPSSPPHeadless has no macOS build).
Isolated HOME in work/pphome (never the user's ~/.config/ppsspp), sound off, WebSocket debugger on PORT.

    pp.py start [orig]       boot build/NPJJ30029 (or rom/NPJJ30029 with "orig"), print PID
    pp.py fb OUT.png         screenshot from PSP video memory (works when "shot" does not), leaves the game running
    pp.py stop               kill by PID
    pp.py shot OUT.png       screenshot through the debugger
    pp.py call EVENT [k=v..] raw debugger call, prints the JSON reply (values parsed as JSON when possible)
    pp.py mem ADDR SIZE OUT  dump PSP memory to a file
    pp.py keys "BTN+BTN" FRAMES   hold buttons for FRAMES (60 Hz wall clock), then release

shortcut: wall-clock input, not frame-exact; build the agent-qa headless fork if routes need determinism."""
import base64, glob, json, os, re, shutil, signal, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill import SKILL  # noqa: E402
sys.path.insert(0, os.path.join(SKILL, 'scripts'))
import psp  # noqa: E402

PORT = 43117
HOME = os.path.join(ROOT, 'work', 'pphome')
SYS = os.path.join(HOME, '.config', 'ppsspp', 'PSP', 'SYSTEM')
PID = os.path.join(ROOT, 'work', 'pp.pid')
EXE = os.path.join(ROOT, 'tools', 'ppsspp', 'PPSSPPSDL.app', 'Contents', 'MacOS', 'PPSSPPSDL')
INI = {'RemoteDebuggerOnStartup': 'True', 'RemoteISOPort': str(PORT), 'Enable': 'False', 'GlobalVolume': '0',
       'FirstRun': 'False', 'FullScreen': 'False',
       'SoftwareRenderer': 'True'}   # the Vulkan backend fails gpu.buffer.screenshot ("Could not download output")


def set_ini():
    os.makedirs(SYS, exist_ok=True)
    p = os.path.join(SYS, 'ppsspp.ini')
    txt = open(p, encoding='utf-8-sig').read() if os.path.exists(p) else '[General]\n[Sound]\n[Graphics]\n'
    for k, v in INI.items():
        txt, n = re.subn(r'(?m)^%s = .*$' % k, '%s = %s' % (k, v), txt)
        if not n:
            sec = '[Sound]' if k in ('Enable', 'GlobalVolume') else '[Graphics]' if k == 'FullScreen' else '[General]'
            txt = txt.replace(sec, '%s\n%s = %s' % (sec, k, v), 1)
    open(p, 'w', encoding='utf-8').write(txt)


def ws():
    return psp.WS(PORT, timeout=60)


def main():
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == 'start':
        iso = glob.glob(os.path.join(ROOT, 'rom', '*.iso'))[0]
        # the game data is CONTENT.DAT on the memory stick: install the wanted copy (orig = rom/, else build/)
        src = os.path.join(ROOT, 'rom' if a and a[0] == 'orig' else 'build', 'NPJJ30029')
        dst = os.path.join(HOME, '.config', 'ppsspp', 'PSP', 'GAME', 'NPJJ30029')
        shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst)
        set_ini()
        log = open(os.path.join(ROOT, 'work', 'pp.log'), 'w')
        p = subprocess.Popen([EXE, os.path.abspath(iso)], stdout=log, stderr=log, env=dict(os.environ, HOME=HOME),
                             start_new_session=True)
        open(PID, 'w').write(str(p.pid))
        print('pid', p.pid)
    elif cmd == 'stop':
        try: os.kill(int(open(PID).read()), signal.SIGKILL)
        except (OSError, ValueError) as e: print('not running:', e)
    elif cmd == 'shot':
        w = ws()   # the screenshot call needs the CPU stopped; cpu.stepping answers with an event, not a ticket
        if not w.call('cpu.status')['stepping']:
            w._send(1, json.dumps({'event': 'cpu.stepping'}).encode()); w.wait('cpu.stepping')
        r = w.call('gpu.buffer.screenshot')
        open(a[0], 'wb').write(base64.b64decode(r['uri'].split(',')[1]))
        w.call('cpu.resume')
    elif cmd == 'fb':
        from PIL import Image
        d = ws().mem(0x04000000, 512 * 272 * 2)   # displayed buffer: 16-bit 565, stride 512, red in the low bits
        im = Image.frombuffer('RGB', (512, 272), d, 'raw', 'BGR;16', 0, 1)
        b, g, r = im.split()
        Image.merge('RGB', (r, g, b)).crop((0, 0, 480, 272)).save(a[0])
    elif cmd == 'call':
        kw = {}
        for x in a[1:]:
            k, v = x.split('=', 1)
            try: kw[k] = json.loads(v)
            except ValueError: kw[k] = v
        print(json.dumps(ws().call(a[0], **kw), indent=1)[:6000])
    elif cmd == 'mem':
        w = ws(); addr, size = int(a[0], 16), int(a[1], 16)
        with open(a[2], 'wb') as f:
            for o in range(0, size, 1 << 20):
                f.write(w.mem(addr + o, min(1 << 20, size - o)))
    elif cmd == 'keys':
        w = ws(); keys = set() if a[0] == '-' else set(a[0].split('+'))
        w.call('input.buttons.send', buttons={k: (k in keys) for k in psp.BUTTONS})
        time.sleep(int(a[1]) / 60)
        w.call('input.buttons.send', buttons={k: False for k in psp.BUTTONS})


main()
