# Glossary and style

Base script: LIPEMCO! Translations (TheMajinZenki), `vendor/tenmatools/tenma/script/`. Our changes are rules in
`tools/restyle.py`, applied at build time; the vendored script stays as upstream wrote it.

## Terms (ruled by the user)

| Japanese | English | Note |
|---|---|---|
| ジパング | Jipang | the world; never Japan/Zipang for the setting |
| 徳 | Virtue | experience points |
| 両 | Ryo | money, capitalised; in dialogue the amount comes first ("20 Ryo"), never the kanji as a sign. Windows keep `18両` |
| 自来也 | Ziria | the hero, as in the title |

## Names

- Hepburn without long vowels: Koumon -> Komon, Goumon -> Gomon, Mutekiou -> Mutekio, Fuurinkazan -> Furinkazan.
  The full list is `NAMES` in `tools/restyle.py`; add a name there, never by hand in a CSV.
- Unchanged from LIPEMCO: Ziria, Tsunade, Orochimaru, Masakado, Yashahime, Tsukihime, Jashinsai, Guronushi.
- Credits keep real people's names as upstream has them.

## Honorifics (dropped)

- `X-sama` -> `Lord X` (`Lady X` for Yashahime, Tsukihime, Tsunade); after a title (Priest, Hero, Brave) just `X`.
- `X-san`, `-chan`, `-kun`, `-dono` -> `X`.
- Every rule is the same length or shorter than the original, so upstream's line fitting still holds.
