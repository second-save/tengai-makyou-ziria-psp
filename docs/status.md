# Status (2026-11-19)

An English build exists: `build/NPJJ30029/CONTENT.DAT`, sha1 `babc0728a58107cc90e361e0c81c1e62826dca3f`.
Patch for testing: `dist/ziria-psn-en.xdelta` and `dist/ziria-psn-en.zip` (`tools/release.sh`: xdelta3 against
the original `CONTENT.DAT`, re-applied and compared). Everything is committed. Nothing is published.

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

1. First boss-style fight, done: Kinta the Tanuki in the Namazu Shrine (session `en2`, steps 158-168). Clean:
   the sandal scene, the betrayal speech ("You'll never defeat Lord Masakado!"), fight messages with the long
   name ("Kinta the Tanuki took 3 damage!"), and the surrender speech about the giant tweezers. To trigger it:
   bring Kinta in, walk up the corridor left of the chest loop (sandal scene), go on to the tanuki guard, then
   walk back to Kinta. Session `en2` (build `babc0728`) is at step 169: level 6, in the shrine after the fight.
   Still unseen: the bosses of `script_boss.csv` (the first is the Nue, well past Tsuchiura and Mito) and
   everything after the shrine.

   The floor below the shrine, done (session `en2`, steps 170-201, now upstairs beside the crumbled boulder).
   Clean: "There is a large casket here. / It's locked tight.", the upstairs casket ("You look inside the
   casket.", "You found the Tanuki Key!", "Obtained Tanuki Key.", "Acquired 6 Virtue!"), the item list with the
   narrow font for long names (Map of Tsukuba, Giant Tweezers), "You lift the lid of the casket. / There is a
   pair of giant tweezers inside.", "Obtained Giant Tweezers.", "Acquired 8 Virtue!", "Ziria used the Giant
   Tweezers!", "But nothing happened!" (wrong tile), and Namazu's picture scene ("Ouch! Owww!", "Namazu thrashes
   about, causing an earthquake!" on two lines). Battles on the way: Oni-danuki and Sword Bug, up to three
   enemies, clean. How to: the Tanuki Key is in the upstairs casket (menu Check, facing it); downstairs use the
   key from Items facing the locked casket; use the tweezers standing on the left spit directly above Namazu,
   facing down.

   Open question: both "Obtained X." lines print twice (the box clears and types the same line again before the
   Virtue line; only one item is given). Not compared with the original: replaying the `en` + `en2` presses on
   the Japanese build had drifted by frame 66,000 (hero still on Mount Tsukuba), so that method does not work
   over a long route. The shop's "Obtained Map of Tsukuba." printed once.

   Shrine exit to Tsuchiura, done (session `en2`, steps 202-226, now inside the Tsuchiura inn, HP 15/30,
   saved to TENGAI1 on the session memstick). Clean: overworld battles with new enemies (Earth Snake, Daimon
   Acolyte, the two-name target list, "Earth Snake sprang forward" ambush), the location windows "Tsukuba",
   "Tsuchiura Town" and "Inn", the "INN" sign graphic, and the record keeper: "Good day! Would you like me to
   keep a record of your progress? / No need to pay - it's free!", Yes/No, "Let me write this down.", the
   "Backup RAM Data" screen (TENGAI1-4, "New Game", "Choose where to write the file."), "Now writing to
   TENGAI1.", "Write complete." Route: past the rubble take the ladder at the end of the south-east corridor,
   follow the path south then east; the town is the blue castle by the bridge. The record keeper stands right
   of the inn's entrance corridor. Also clean (steps 227-230): the Kumogiri villager beside the item shop, with portrait
   ("Ziria, right? / I'm from Kumogiri Hamlet.", "Just remember this: we're all on your side!"). Tsuchiura's three shops, done (steps 231-254, session now inside the armory with its buy list open,
   953 Ryo). Clean: the general store (bag sign: "Welcome, welcome! / This is my general store. / Tell me what
   you need!", Toad Oil / Rope Sandals / Map of Tsukuba, "Toad Oil, is it?", "Obtained Toad Oil.", "18 Ryo,
   please. / Would you like anything else?", "Thank you, thank you! / See you soon"); the warehouse (two-arrows
   sign: "Hey, welcome to the warehouse! / How can I help ya?", Store/Withdraw Money, Items, Jutsu, the Savings
   and Money windows, "You can store 1,000 Ryo at a time, up to a total of 65,000 Ryo. How about it?", "That's
   1,000 Ryo! / Will you leave more?", "Looks like you don't have 1,000 Ryo on you, friend!", "You can
   withdraw 1,000 Ryo at a time.", "Here's your 1,000 Ryo.", "Whoops! There's nothing to withdraw!", "Our
   service is nationwide! ..."); the armory (sword sign: "Welcome to my armory! / How can I help you?", Long
   Sword, Cloth Katabira, Shinobi Katabira in the narrow font, Leather Helmet, "60 Ryo, please."). In shops
   "Obtained X." prints once. Shop doors are entered from the tile below; trees beside the doors block, so come
   up the gap between them. In a shop, stand on the cushion in the keeper's column. 

   Lord Komon, done (steps 255-271, session now in his room on the castle's top floor, level 6, HP 15/30,
   953 Ryo, Aoi Sword and Shinobi Katabira held). Clean: the Equip screens ("In hands", "On body", "On head",
   "Nothing available."), the old villager with portrait ("You're a Fire Hero, right? / Please, you hafta save
   Lord Komon!", "He's in the castle! I beg ya, help the poor fellow!"), and Komon's whole scene over the
   full-width picture: "Hoh hoh hoh! My name is Komon! / You must be Ziria, the Fire Hero!", "the foreign Cult
   of Daimon is invading Jipang, their aim the resurrection of Masakado!", the Yes/No question, "So you're
   willing to fight against the Daimonists!", "I will have the eastern bridge lowered at once.", "I bestow
   upon you the Aoi Sword, handed down in my family for 200 years!", "You have accepted Komon's request.",
   "Acquired 15 Virtue!", "Obtained Aoi Sword." (printed once). The castle is over the bridge on the town's
   east side: straight up through two rooms, Komon is the middle figure on the dais. Not done in Tsuchiura:
   the inn stay (the innkeeper was not found; the room right of the inn door holds the record keeper), the
   "No" answer to Komon. 

   Eastern bridge and Bokuden, done (steps 272-297, session now in Bokuden's hut after the duel). Clean: the
   three-column item list, the Status screen (Equipment, Virtue 331/381, Attack, Defense, Speed), "Ziria used
   the Toad Oil!", "Ziria recovered 30 HP!", "Tsuchiura Castle" in the location window, "Daimon Acolyte sprang
   forward!", and Bokuden: "I am Bokuden, master of the blade! / If you can defeat me, I will teach you a
   special technique! Up for a fight?", Yes/No, the duel ("Bokuden took 3 damage!", "BOKUDEN SLASH!! / The
   sword's sharpness increased!"), the loss ("Ziria received deep wounds and became unable to fight." in red,
   "Tch! You weakling! / Come back after you train some more!", "In preparation for a new battle, Ziria used
   half his money to fully heal all wounds!", respawn at the record keeper), and the win ("By emptying your
   mind of needless thoughts, you can increase the sharpness of your blade! That is the Bokuden Slash!",
   "The way of the sword is long and steep!", "You have learned the special technique Bokuden Slash."). Not
   captured: the messages at the moment Bokuden falls. Left Japanese: a small wall plaque with brush strokes
   in Bokuden's hut (background art, not ruled on).

   **The `en2` session is poked from step 294 on**: HP and max HP 999, Attack 200 (`poke.py set ...
   0x096667E4=E703 0x096667E8=E703 0x096667FA=C800`), because level 6 cannot beat Bokuden (he deals 6-12 a
   turn and takes 3). Fine for reading text, not for judging balance. Poke before a battle starts: a battle
   already running writes its own HP back. Hero block, further offsets: Attack `+1A`, Defense `+1C`, Speed
   `+1E` (2 bytes each). Route: leave Tsuchiura by its east edge (the road below the castle bridge), cross
   the bridge, the hut is the red house north-west of the far bridgehead; inside, step up onto the raised
   floor through a cushion and stand below Bokuden.

   Kumogiri Hamlet 1, part done (steps 298-326, session now inside the hamlet's inn, level 7, 973 Ryo). Clean:
   the level-up after the duel ("Gained 1 Speed", "HP and TP fully restored! / You're one step closer to
   bringing down the Cult of Daimon."), the location windows "Bokuden's House", "Kumogiri Hamlet 1" and "Inn",
   two villagers ("We've been waiting for you, Lord Ziria! / This is Kumogiri Hamlet, your ally against the
   Daimonists.", "Wow! You must be Ziria! / The Chief told us about you!", "We're all your allies here! / You
   can take it easy!"), the inn stay, seen at last ("Welcome to the inn!", "It's 5 Ryo for the night. / Will
   you stay?", "Please rest well.", "Take care of yourself, Lord Ziria."), the record keeper's No branch
   ("Come back anytime!"), and two inn guests ("A famous fencer called Bokuden lives in a small house west of
   here.", "He's looking for a worthy successor to a special technique of his own design.", "From what I've
   heard, Chief Kumogiri, the founder of our hamlet, was a pupil of the Toad Hermit, just like you."). The
   hamlet is due east of Bokuden's house through the forest (about 27 tiles); in its inn the blue figure is the
   innkeeper, the one left of the hearth the record keeper. Also clean (steps 327-341, session now outside the hamlet's general store, 985 Ryo): the statue villager
   ("The statues in the middle of our hamlet represent the Fire Clan.", "Everyone here respects the Fire Clan. /
   Good luck, Ziria."), and the general store's selling side, first time seen ("What will you be selling?",
   the belongings list, "That will be 12 Ryo. / How does that sound?", Yes/No, "Will you be selling anything
   else?", and the key-item refusal "Giant Tweezers? How much would that be worth? I'm afraid I can't really
   tell."), plus its buy list (Toad Oil, White Toad Oil, White Crane Plume, Map of Tsukuba). Kogama, done (steps 342-346): the green frog between two stones on the hamlet's
   east side, level with the southern houses ("Hey, Ziria! You look well! / Traveling alone is dangerous, so I
   decided to come with you!", "I can reach any Kumogiri Hamlet I've visited at least once in a single leap!",
   "I'm incredibly useful - you'll see! / Now let's go kick Masakado's butt!", "Kogama, your helper, has joined
   your quest.", "Acquired 13 Virtue!"), and the Kogama command inside the hamlet ("You can't use that here.").
   More of the hamlet (steps 347-360, session now inside the Thieving School, the left-hand southern house):
   the priest's son with portrait ("I-I need your help! / I'm the son of the priest of the Kashima Village
   shrine, to the east.", "The Daimonists turned the sacred White Deer, protector of our village, into
   stone!"), the villager between the southern houses ("Kogama, one of the frogs from the Toad Hermit's place,
   came to our hamlet looking for you.", "He's a brave little frog. Can you believe he came all the way here on
   his own?"), and the Thieving School's instructor ("If you can steal the money successfully, you get to keep
   it for yourself!", "Think of it as a game and have fun! / But don't forget your quest to defeat Masakado!")
   with the location window "Thieving School". The right-hand southern house has a closed wooden door that
   does not open. The school's master, on the raised floor (steps 361-367): "This is a Thieving School, where you
   can improve your thievery in order to help defeat the Cult of Daimon!", "Head inside, avoid the instructors,
   and steal the money from the casket!" - all four of the school's lines are now seen. The game room is
   through the door behind the master: three patrolling instructors; touching one puts the hero back in the
   front room with no message (the script has none). The casket sits behind the crate row; the way in looks
   like the top row, then the left column down to the row under the counter. Not done: reaching that casket
   (its reward line).

   Hamlet to Kashima Shrine, done (steps 368-382, session now just inside Kashima Shrine's entrance, level 7,
   HP 23/53, 1018 Ryo). Clean: new enemies Yato, a pair of tanuki and Daimon Priest ("Yato took 5 damage!",
   "Daimon Priest's attack!", "Ziria dodged."), the location window "Kashima Shrine", and the Kogama command
   on the overworld: it shows a map of Jipang with the current province lit, then returns (one hamlet known,
   nothing to choose). The map's corner caption is decorative cursive, not readable text; not compared with
   the original. The level-up at step 298 reset the poked stats (HP 53, normal Attack), so play is unpoked
   again from there. Route: leave the hamlet by its east exit (between the two stones, one row above the
   southern houses' doors), follow the beach south-east down the sandbar, cross the bridge east at its top;
   the shrine is the red torii just past the bridge. 

   Kashima Shrine, part done (steps 383-399, session now at the armory counter with the buy list open,
   1013 Ryo). Clean: four villagers ("The White Deer, the guardian deity of Kashima Village, was turned into
   stone by the Daimonists!", "We won't survive long without his divine protection! What should we do?!";
   "I once fell from a tree and got hurt, but then the sacred White Deer healed me with his divine
   powers...", "Please, you have to save him!"; "The Daimonists feared the divine powers of the White Deer, so
   they turned him to stone.", "I can hear his sorrowful voice coming from within the rock..."; "The White
   Deer's divine powers can heal minor illnesses and light injuries in a few moments.", "He was trying to
   entrust the Fire Hero with a scroll containing that divine power, but now..."), and the armory (Samurai
   Sword, Shinobi Katabira, Leather Helmet, Shuriken; "Shuriken, is it?", "Obtained Shuriken.", "5 Ryo,
   please. / Would you like anything else?"). Layout: inn on the lower terrace left of the steps, armory and
   general store on the middle terrace, more above. The armory door is entered from the row below it, coming
   from the path side. Not done: the general store, the inn, two villagers on the top terrace, the tanuki
   lines, the White Deer's stone (red stone with the 大 mark: the script keeps the kanji in "There is a large
   red stone marked with a yellow 大 symbol." - check how it renders). Then Mito ("just north from here,
   beyond the lake").
2. Money, done as ruled (`docs/decisions.md`): `restyle.py` `money()` turns upstream's "両20" into "20 Ryo" in
   every English line (176 lines, five script files); windows keep "18両". Seen in game: "2 Ryo, please.",
   "15 Ryo, please.", "It's 4 Ryo for the night.", "Ziria obtained 2 Ryo." The bank lines with "65,000 Ryo" were
   seen later in Tsuchiura's warehouse, clean.

Seen clean on build `babc0728` (session `en2`): the inn (price, Yes/No, "Please come again."), the field menu
entries Items (Use/Give/Drop, "Ziria used the Map of Tsukuba!"), Equip ("In hands", "On body"), Jutsu, Kogama,
Check, Mode (Descriptions, Walk Type, Text Speed, Text Skip), Status, the Armory (Buy Wares / Sell Belongings,
Long Sword, Cloth Katabira, Leather Helmet), and a full level-up ("Ziria rose to level 2!", "Gained 1 Attack!",
"HP and TP fully restored!").

Later in `en2` (steps 45-123): eleven Tsukuba Village villagers, two with portrait panels, a house villager,
a chained level-up to level 6 and a two-enemy cave battle (Sword Bug), all clean. The cave whose entrance is the
dark hole south-west of the village (from the village exit: left 3 tiles, down 8) is the Namazu Shrine; a tanuki
guards its chest ("You're not going anywhere, pon!"). Kinta is a small red villager who wanders the village's
north-west path; his cutscene (full-width portrait, five pages, "Kinta has joined you!") is clean. Step 141 =
Kinta just joined, hero at the north end of the west path. Next story beat: back to the shrine, where Kinta
turns on the hero (`map-0x124F-0x38E`). Dialogue tip: Circle on the
last page closes the box, one press more opens the field menu, so count pages or alternate circle and cross.

Left Japanese, found this session: the Map of Tsukuba screen has a red seal with the kanji 筑波 drawn in the
picture. Upstream left it. Ruled: leave it (`docs/decisions.md`).

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
