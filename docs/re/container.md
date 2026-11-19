# Container (PSN "Virtual PC Engine", NPJJ30029)

The PSP ISO is only the emulator (`EBOOT.BIN`, module `psnvpce`, "Virtual PC Engine for PSP Network"). The game is
`ms0:/PSP/GAME/NPJJ30029/CONTENT.DAT` (path from `USRDIR/CONFIG.PSP`). A patch only has to replace `CONTENT.DAT`.

## Layers, outside in

1. **XOR, 512-byte key repeating from file offset 0** (`tools/content_xor.py`). The key is recovered from the file:
   the most repeated 512-byte unit is 0xFF padding. The dump's last 28 bytes are zeros added after the XOR.
   `psp-key.edat` (16 bytes) is not used for this layer.
2. **Archive** (`tools/vpce.py`): 0x80 header (magic `12 34 56 78`, entry count u32 at 0x28; bytes 0x04-0x1F and
   0x2C-0x7F unknown, kept as is), 31 entries of 0x50 bytes (name[0x40], offset u32, size u32), data 16-aligned.
   Files: `CONFIG.PS3`, `HCD9005.hcd`, `HCD9005_01/03/04/05.at3` (audio), `HCD9005_02/06.bin` (data),
   `HUDSON.GIM`, `WALL.GIM`, `psp_001..018.png` (manual), `SAVEDATA.PNG`, `SNDBANK0.PSM`, `SYSCARD3P.PCE`.
3. **Data track** (`tools/hcd.py`): u32 chunk count, count x (u32 offset, u32 stored size), each chunk a zlib
   stream (level 9) of 0x40000 bytes of cooked 2048-byte sectors, zero-padded to 4 bytes.
4. **PC Engine CD data track**, 62972 sectors (track 02; track 06 is a near copy, 62822 sectors).
   `HCD9005.hcd` is the track sheet: `trackNN,audio|code,file,start frame,length`.

## Facts checked

- `tools/build.py --identity` rebuilds `CONTENT.DAT` byte-identical.
- **No integrity check:** a build with one changed byte in track 02 boots to the game's title screen in PPSSPP
  (the unknown header bytes are not a hash of the tracks, or are not checked).
- The System Card checks the IPL string `PC Engine CD-ROM SYSTEM` (sector 1): changing it hangs at JUST A MOMENT.
- Track 02 and 06 are byte-identical to the Ziria tracks of the PSP "Tengai Makyou Collection"
  (sha1 `27111a52…` and `d5c66db2…`): one translated track serves both products.
- Track size must not change (the sheet holds lengths; the game addresses sectors directly, no ISO9660).

## PPSSPP on this Mac

The skill's headless build is Windows-only. `tools/pp.py` drives the stock SDL build: isolated `HOME` in
`work/pphome` (XDG_CONFIG_HOME is ignored on macOS), software renderer, debugger on port 43117.
`pp.py fb` reads the frame from PSP video memory (16-bit 565, stride 512), because `gpu.buffer.screenshot`
fails. First boot asks seven emulator prompts; `tools/fixtures/SAVEDATA` is the save made after them.
