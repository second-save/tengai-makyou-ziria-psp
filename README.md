# Tengai Makyou Ziria (PSN PC Engine Archives, NPJJ30029): English patch

An English patch for the PSN "PC Engine Archives" release of *Tengai Makyou Ziria* (PSP, NPJJ30029).
It is a port of the LIPEMCO! Translations patch for the PC Engine CD game, with names and terms restyled
(`glossary.md`). The patch holds no game data: you need your own copy of the game.

**Status: test build.** Checked in PPSSPP 1.20.4 only: the emulator's first-run prompts, System Menu and all 18
manual pages; in the game, a playtest up to the Riku region. Not checked: the rest of the game, real PSP hardware.

## What changes

- The game itself is in English, with a variable-width font.
- No honorifics: `-sama` becomes Lord or Lady, the other suffixes are dropped.
- Shorter names (Koumon -> Komon). World = Jipang, experience = Virtue, money = Ryo.
- The emulator's own prompts and menus (save, load, screen size, autosave, the L-button System Menu), the
  18 manual pages and the XMB title and picture are in English too.
- Not translated: pictures from the game inside the manual pages (old Japanese screenshots), and the logos.

## Apply the patch

Two patches, for the two files of the release (an unmodified dump of each is needed):

| File | Original SHA-1 | Patched SHA-1 | Patch |
|---|---|---|---|
| `NPJJ30029/CONTENT.DAT` (the game, decrypted as PPSSPP reads it) | `1a009332f54e283bfaedff5d073008a60b9b06c7` | `5106f44801aed9578c90f3df4099cf22c7f8ef05` | `ziria-psn-en.xdelta` |
| the ISO (`Tengai Makyou - Ziria (JPN) (PCE) (PSN) [NPJJ30029].iso`) | `a7ae6b1bb260264a03b7798ac4fad77fc51c778e` | `3c6fb39f1a50803d9bf14fcadafc9df952202490` | `ziria-psn-en-iso.xdelta` |

    xdelta3 -d -s CONTENT.DAT ziria-psn-en.xdelta CONTENT.en.DAT
    xdelta3 -d -s "Tengai Makyou - Ziria (JPN) (PCE) (PSN) [NPJJ30029].iso" ziria-psn-en-iso.xdelta "Tengai Makyo Ziria (English).iso"

Rename `CONTENT.en.DAT` to `CONTENT.DAT` and put it in `PSP/GAME/NPJJ30029/` on the memory stick, in place of
the original. Keep a copy of both originals. In PPSSPP, start the English ISO.

The English ISO's program (EBOOT) is not signed yet: it runs in PPSSPP, not on a real PSP or Vita. The
`CONTENT.DAT` patch alone works with the original ISO (game in English, emulator prompts in Japanese).

## Build from source

Needs python 3, g++, make, cmake, libpng, ImageMagick and xdelta3. See `AGENTS.md` for the commands and
`docs/status.md` for how the build works. `tools/build_en.sh` runs the whole build (about 12 minutes).

## Credits

- Original English patch: LIPEMCO! Translations. Supper (hacking), TheMajinZenki (translation), cccmar and
  rg111 (testing). Source: `suppertails66/tenmatools`, vendored in `vendor/tenmatools`.
- PSN port, restyle, prompts and manual: second-save. Manual font: M+ 1p (SIL OFL, `fonts/OFL.txt`).

## Licence

GPLv3, as the patch it is built from (`vendor/tenmatools/COPYING`). *Tengai Makyou Ziria* belongs to its
rights holders; this project is not affiliated with them.
