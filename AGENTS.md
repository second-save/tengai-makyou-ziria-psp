# Tengai Makyou Ziria (PSN PC Engine Archives, NPJJ30029): English translation

A second-save project. No game data in git (`rom/`, `work/`, `build/` are ignored).
Read `docs/status.md` (state, next step) and `docs/decisions.md` (the user's rulings) first.

## Commands (python = `tools/venv/bin/python`; create with `python3 -m venv tools/venv && pip install capstone pillow pyelftools`)

- Check the dump: `shasum -c rom.sha1`
- Identity test: `python tools/build.py --identity` (must print `identity OK`)
- Build: `python tools/build.py` -> `build/NPJJ30029/CONTENT.DAT` (game + manual) and `build/ziria_en.iso` (prompts)
- Boot the build: `python tools/pp.py start` (`start orig` for the original), `pp.py fb OUT.png`, `pp.py keys cross 8`,
  `pp.py stop`. Frame-exact play: `tools/play.sh` (see `docs/status.md`); there Circle confirms. Stock PPSSPP 1.20.4 in `tools/ppsspp/` (`fetch_emu.py ppsspp`, then
  `chmod +x` the binary); it runs with `HOME=work/pphome`, never the user's own PPSSPP folder.
- EBOOT signer (needed by build.py): `bash tools/build_sign_np.sh` -> `work/src/sign_np/sign_np`;
  decrypted original EBOOT in `work/eboot_jp.elf` (see `tools/frontend.py`).
- Full English build: `PY=tools/venv/bin/python bash tools/build_en.sh` (12 minutes). Patch + zip: `tools/release.sh`
- Skill path: `python tools/skill.py`

## Layout

- `rom/` the user's dump: PSP ISO (emulator only) + `NPJJ30029/CONTENT.DAT` (the game).
- `tools/content_xor.py`, `vpce.py`, `hcd.py`: the three container layers (`docs/re/container.md`).
- `work/ziria_02.iso`: unpacked PC Engine CD data track (2048-byte sectors), the thing to hack.
- `tools/fixtures/SAVEDATA`: emulator save made after the first-run prompts (the suspend file `NPJJ30029GAME1/PSNVPCE1.SAV` is a memory snapshot: kept local, not in git; boot once and save at the prompt to make one).
- `script/eboot.csv` emulator prompts; `tools/manual.py` manual pages; `fonts/` M+ 1p (OFL).

## Rulings

- English, variable-width font. World = **Jipang**, XP = **Virtue**, money = **Ryo**. Prefer shorter names.
- Never push or publish without the user's say-so; publish under the `second-save` org.
- The work is PC Engine CD romhacking (HuC6280), not PSP text work.
