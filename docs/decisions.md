# Decisions

## Ruled by the user (2026-11-19)

- English, with a variable-width font.
- World = **Jipang**, XP = **Virtue**, money = **Ryo**.
- Be mindful of names; favour shorter ones.
- Publish under the `second-save` org (standing preference).

- **Base: port LIPEMCO's patch** (script + VWF, GPLv3) to this disc revision, then edit names and terms to the
  rulings above. Rejected: a fresh translation with our own VWF (fully ours, many times the work). The result
  stays GPLv3 and credits LIPEMCO (Supper, TheMajinZenki, cccmar, rg111).
- **Honorifics: dropped.** No -sama/-san/-dono; titles such as Lord or Master where needed. Rejected: keeping
  them as LIPEMCO has them.
- **Money sign: spell out "Ryo" in dialogue** ("両2, please." -> "2 Ryo, please.", 176 lines). Windows keep the
  kanji after the number ("18両"), as the option said. Rejected: redrawing the 両 glyph as a Latin sign (Claude's
  recommendation: one font change, no longer lines); keeping 両 everywhere as LIPEMCO has it.
- **Scope: game only.** The patch replaces `CONTENT.DAT` alone. The Virtual PC Engine prompts (would need a
  patched, re-signed EBOOT) and the 18 manual pages stay Japanese.
