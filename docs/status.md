# Status (2026-11-19)

An English build exists: `build/NPJJ30029/CONTENT.DAT`, sha1 `babc0728a58107cc90e361e0c81c1e62826dca3f`.
Patch for testing: `dist/ziria-psn-en.xdelta` and `dist/ziria-psn-en.zip` (`tools/release.sh`: xdelta3 against
the original `CONTENT.DAT`, re-applied and compared). One commit exists (`a28eb6c`); the work after it
(`tools/play.sh`, `tools/release.sh`, `README.md`, the money rule) is uncommitted. Nothing is published.

## Checked in PPSSPP (stock 1.20.4, macOS)

- Title screen, save menu, intro subtitles, first cutscene, field menu, Status screen (Virtue), talking to an NPC:
  all English, variable-width font, no garbling.
- The final build (after the last packing change) was booted again to the title and the intro.

Not checked: battles (the hero got stuck on a gatepost with wall-clock input), shops, anything past the first
room, real PSP hardware. One boot attempt quit during the emulator prompts and did not reproduce; the same
steps worked on the next run (wall-clock input, see Open).

## How the build works (`tools/build_en.sh`, one command, about 12 minutes)

1. `CONTENT.DAT` -> data track (`docs/re/container.md`; `tools/build.py --identity` is byte-identical).
2. `tools/make_rev7.py`: the track becomes Redump **Revision 7** by writing the 18 code blocks from
   `vendor/tenmatools/tenma/base/` over ours. The two revisions differ only there as far as checked: all 19
   disc-sourced files in tenmatools' `rsrc_raw/` occur whole in our track. So no code porting was needed.
3. `tools/restyle.py`: LIPEMCO's script with our rulings (1,235 lines changed; rules in `glossary.md`).
4. LIPEMCO's own build (`vendor/tenmatools`, GPLv3, copied to `work/tenmatools`) makes the translated track.
5. `tools/build.py` packs it as track 02 into `CONTENT.DAT`. Track 06 stays, as upstream. `tools/vpce.py` keeps
   later files at their offset modulo 512 so their encrypted bytes do not change.

Local fixes to the vendored source, both needed on macOS: a copy-assignment operator for
`TThingyTable::EntrySuffixMapEntry` (segfault in `tenma_scriptbuild` with libc++), and `-pedantic` instead of
`-pedantic-errors` in `wla-dx/CMakeLists.txt` (plus `-DCMAKE_POLICY_VERSION_MINIMUM=3.5` for CMake 4).
Build needs: g++, make, cmake, `brew install libpng imagemagick`; `xdelta3` for the patch.

## Facts

- The disc is byte-identical to the Ziria tracks of the PSP Tengai Makyou Collection
  (`~/develop/tengai-makyou-collection-psp`): `work/tenmatools/tenma/tenma_02_build.iso` drops into that project.
- No PSP version of the LIPEMCO patch existed. Credits: Supper (hacking), TheMajinZenki (translation),
  cccmar and rg111 (testing).

## Frame-exact play (added later on 2026-11-19)

`tools/play.sh new NAME [orig]` then `tools/play.sh NAME PRESSES.. [--wait N --every N]` wraps the skill's `play.py`
on the headless PPSSPP fork built in `~/develop/tengai-makyou-collection-psp/tools/ppsspp-headless/` (env
`PPSSPP_HEADLESS` overrides). Here **Circle confirms** (PC Engine I) and Cross does nothing on the save menu.
Session `work/play/en` (English build): step 13 = control in the first room (copy: `work/first_room.ppst`),
step 18 = first random battle, command menu open. Seen in English with no garbling: full intro narration, the
first cutscene, the new-file message, the battle command menu (Attack/Jutsu/Item/Steal/Defend/Flee) and HP/TP
header. The intro cannot be skipped (about 25,000 frames). Random battles start after ~20 s of pacing below
Mount Tsukuba; the first village is the building just left of the mountain exit.

Also seen clean, same session: the whole first battle to "Acquired 1 Virtue!" (step 21), a three-page villager
dialogue in Tsukuba Village (steps 32-36), the General Store (steps 44-47: greeting, buy list, "Map of Tsukuba,
is it?" Yes/No, "Obtained Map of Tsukuba."). Walking is tile-snapped, 16 frames a tile; shop doors are the green
ones and need the exact column. In zsh pass each press as its own argument (an unsplit `$P` makes `emu.py`
exit 2).

## Next

1. The first boss (`script_boss.csv` text has not been seen in game). Nobody knows the route yet; use
   `tools/poke.py` to keep HP up. Session `work/play/en2` (build `babc0728`) is at step 44: level 2, Long Sword,
   986 Ryo, on the overworld below Tsukuba Village.
2. Money, done as ruled (`docs/decisions.md`): `restyle.py` `money()` turns upstream's "両20" into "20 Ryo" in
   every English line (176 lines, five script files); windows keep "18両". Seen in game: "2 Ryo, please.",
   "15 Ryo, please.", "It's 4 Ryo for the night.", "Ziria obtained 2 Ryo." Not seen: the bank lines with
   "65,000 Ryo"; the build re-wraps them, but nobody looked.

Seen clean on build `babc0728` (session `en2`): the inn (price, Yes/No, "Please come again."), the field menu
entries Items (Use/Give/Drop, "Ziria used the Map of Tsukuba!"), Equip ("In hands", "On body"), Jutsu, Kogama,
Check, Mode (Descriptions, Walk Type, Text Speed, Text Skip), Status, the Armory (Buy Wares / Sell Belongings,
Long Sword, Cloth Katabira, Leather Helmet), and a full level-up ("Ziria rose to level 2!", "Gained 1 Attack!",
"HP and TP fully restored!").

Later in `en2` (steps 45-123): eleven Tsukuba Village villagers, two with portrait panels, a house villager,
a chained level-up to level 6 and a two-enemy cave battle (Sword Bug), all clean. Kinta was not found in the
village: his line (`map-0x11A7-0x5F8`) is the one not seen. Step 123 = just inside the cave whose entrance is the
dark hole south-west of the village (from the village exit: left 3 tiles, down 8). Dialogue tip: Circle on the
last page closes the box, one press more opens the field menu, so count pages or alternate circle and cross.

Left Japanese, found this session: the Map of Tsukuba screen has a red seal with the kanji 筑波 drawn in the
picture. Upstream left it. Not ruled on.

Debug tool: `tools/poke.py dump STATE OUT.bin` and `poke.py set STATE_IN STATE_OUT ADDR=HEXBYTES..` work on
`play.sh` savestates (PSP memory, little-endian). Hero block at `0x096667E0`: HP `+4` (2 bytes), TP `+6`,
max HP `+8`, max TP `+A`, level `+C`, Virtue `+D`. Money at `0x09666838`. Level 2 needs 8 Virtue. To use it in a
session, replace the newest `NNNN.ppst` with the poked state.
3. Restyle read, done by pattern, not line by line: 1,063 changed lines, no honorific suffix left anywhere, no
   doubled title ("Lord Lord", "Master Lord"). Most of the 152 "Lord Ziria" lines are the innkeepers' "Take care
   of yourself, Lord Ziria."; the rest are respectful address. Left as is.
4. Release: `README.md` (GPLv3, credits, hashes, install steps) and `tools/release.sh` exist;
   `dist/ziria-psn-en.zip` holds the patch and README for this build. Ask before publishing under `second-save`.
5. Replay check for any new build: `tools/play.sh en --route 47` gives the session's presses; run them with the
   skill's `emu.py ISO --memstick DIR --sav tools/fixtures/SAVEDATA --route-str ...` on a memstick holding the
   new `PSP/GAME/NPJJ30029` (100 s, ends on the shop's price line). It stayed in sync across the text change.

## Open

- `tools/pp.py` input is wall-clock, not frame-exact: walking is imprecise and one run in six misbehaved.
- The patch is 55 MB because the changed track is zlib-compressed and XORed; a patcher that works on the
  unpacked track would be far smaller.
- Real hardware: nobody has booted a modified `CONTENT.DAT` on a PSP. On a console the file is an NPDRM EDAT;
  this dump is its decrypted form, which needs custom firmware that loads decrypted content.
- Emulator prompts and the 18 manual pages stay Japanese (ruled out of scope).
