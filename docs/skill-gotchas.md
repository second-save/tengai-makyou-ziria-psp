# Skill gotchas (one line each: the reference file it belongs in, then the fact)

- `references/platform-psp.md`: a PSN title whose data sits on the memory stick (`PSP/GAME/<ID>/CONTENT.DAT`) runs
  under `play.py`/`emu.py` if the session's `memstick/PSP/GAME/<ID>` is filled before the first step; `play.py`
  does not wipe an existing `SESSION/memstick`.
- `references/emulator-qa.md`: `play.py --route N` output replays on another build with `emu.py --route-str`,
  `--memstick` and `--state-out`; a new `play.py` session then starts from that state with `--state`.
- `references/emulator-qa.md`: `psp.py` has no memory write or cheat hook. `Run.ws.call('memory.write',
  address=, base64=)` works on the headless fork; `tools/poke.py` here wraps it for savestates.
- `references/emulator-qa.md`: in zsh an unquoted `$P` holding several presses is one argument; `play.py` then
  fails with "emu.py exit 2; session unchanged" and no hint about the press syntax.
- `references/platform-psp.md`: PC Engine Archives titles map Circle to button I (confirm) and Cross to II.
