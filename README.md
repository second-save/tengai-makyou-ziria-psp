# Tengai Makyou Ziria (PSN PC Engine Archives, NPJJ30029): English patch

An English patch for the PSN "PC Engine Archives" release of *Tengai Makyou Ziria* (PSP, NPJJ30029).
It is a port of the LIPEMCO! Translations patch for the PC Engine CD game, with names and terms restyled
(`glossary.md`). The patch holds no game data: you need your own copy of the game.

**Status: test build.** Checked in PPSSPP 1.20.4 only: title, save menu, intro, first cutscene, field menu,
Status screen, a battle, villager dialogue and a shop. Not checked: anything after the first village, and real
PSP hardware.

## What changes

- The game itself is in English, with a variable-width font.
- No honorifics: `-sama` becomes Lord or Lady, the other suffixes are dropped.
- Shorter names (Koumon -> Komon). World = Jipang, experience = Virtue, money = Ryo.
- Not translated: the emulator's own prompts (save, load, screen size) and the 18 manual pages.

## Apply the patch

You need `NPJJ30029/CONTENT.DAT` in its decrypted form (the one PPSSPP reads):

| File | SHA-1 |
|---|---|
| `CONTENT.DAT` (original) | `1a009332f54e283bfaedff5d073008a60b9b06c7` |
| `CONTENT.DAT` (patched) | `a9cc6890310d7a7b090c0323e3d4f339acbfc7ec` |

    xdelta3 -d -s CONTENT.DAT ziria-psn-en.xdelta CONTENT.en.DAT

Rename the result to `CONTENT.DAT` and put it in `PSP/GAME/NPJJ30029/` on the memory stick, in place of the
original. Keep a copy of the original. In PPSSPP, start the game's ISO as usual.

## Build from source

Needs python 3, g++, make, cmake, libpng, ImageMagick and xdelta3. See `AGENTS.md` for the commands and
`docs/status.md` for how the build works. `tools/build_en.sh` runs the whole build (about 12 minutes).

## Credits

- Original English patch: LIPEMCO! Translations. Supper (hacking), TheMajinZenki (translation), cccmar and
  rg111 (testing). Source: `suppertails66/tenmatools`, vendored in `vendor/tenmatools`.
- PSN port and restyle: second-save.

## Licence

GPLv3, as the patch it is built from (`vendor/tenmatools/COPYING`). *Tengai Makyou Ziria* belongs to its
rights holders; this project is not affiliated with them.
