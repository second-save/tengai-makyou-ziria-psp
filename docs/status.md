# Status (2026-11-19)

An English build exists: `build/NPJJ30029/CONTENT.DAT`, sha1 `3b8a8289f8cde653cf91a232eb2477149059bc8f`.
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

   Both "Obtained X." lines print twice (the box clears and types the same line again; one item is given).
   Explained later, not a port bug: the game prints a per-map line (23 of them in `script_dialogue.csv`,
   Japanese "Xを 手に入れた") and then the engine's generic line (`script_generic_text.csv` `str-0x134`,
   "[string]を手に入れます"). The Japanese wording differs slightly; upstream translates both "Obtained X.".
   Shops print only the generic one. At the White Deer the two differ ("Obtained Wakakusa." then "Obtained
   Scroll of Wakakusa."). Rewording one of the two is a style choice, not ruled on. The replay of the `en` +
   `en2` presses on the Japanese build drifted by frame 66,000, so that comparison method does not work over
   a long route.

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
   on the overworld: it shows a map of Jipang with the current province lit, then, on Circle, warps to the
   hamlet (confirmed from Kashima's gate at step 445: the hero lands on the hamlet's overworld tile; no text). The map's corner caption is decorative cursive, not readable text; not compared with
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
   from the path side. Also clean (steps 400-418, session now inside the shrine hall on the top terrace,
   977 Ryo): the general store's list (Toad Oil, White Toad Oil, White Snake Stone, Map of Tsukuba), the
   three-column item list with Shuriken, the Kumogiri informant with portrait ("Ziria, right? / I'm from
   Kumogiri Hamlet. / I have new intel on the Daimonists.", "Daimonist tanuki are waiting in ambush for you in
   the northern part of the village.", "I'm sure you'll be fine, but be careful, Ziria!"), the woman in red
   ("Our sacred White Deer is sealed within a rock at the back of the village.", "The Daimonists are guarding
   it... / Be very careful."), and the priest with portrait ("I once read in an old book that the voice of
   the Fire Clan has the power to release all evil seals.", "I'm utterly convinced there must be some sort of
   hint in those words!", "I don't know exactly what it means, but I'm sure that you will be able to solve
   this riddle, Lord Ziria!"). The White Deer, done (steps 419-431, session now in front
   of the red stone, level 7, HP 46/53): the tanuki ambush has no dialogue (a battle with two Oni-danuki
   starts halfway up the avenue of tanuki statues), the stone's Check line renders with its kanji glyph
   ("There is a large red stone marked with a yellow 大 symbol."), and Talk on the stone frees the deer:
   "I'm free! This voice...", "...messenger of the divine! / Thank you for breaking the evil seal of the
   Daimonists!", "The Daimonists are strong...incredibly strong! Masakado is stronger yet! / But I know you
   will defeat them!", "I bestow upon you the scroll of Wakakusa, which contains my divine power!", "The
   Wakakusa jutsu is a technique that can heal minor injuries in a few moments!", "Take down the Cult of
   Daimon! / Prevent Masakado's revival! / Go forth, young Ziria!", "Acquired 10 Virtue!", "Obtained
   Wakakusa.", "Obtained Scroll of Wakakusa." Route: from the shrine hall go right, north into the tree maze,
   left along the first row, up, back right, then down the next column and left to the statue avenue; walk up
   it. Wakakusa in the Jutsu menu (step 434): Use/Give, "Ziria recovered
   7 HP!", 2 TP. After the scene (steps 435-442, session now on the middle
   terrace beside the armory, HP 49/53, 987 Ryo): the stone's Check gives "You find nothing."; the avenue
   ambush fires again on the way back (two more Oni-danuki); and the villager by the armory: "The rock the
   White Deer was sealed inside is red, with a 大 (dai) symbol written on it in yellow!", "It's so glaring, as
   if the Daimonists are proud of their evil! I hope someone defeats them soon!" Not done: the
   woman's tanuki-soup line (`map-0x140F-0x37A`, speaker not found), any changed villager lines after the
   scene, and the inn (`map-0x1447`), which matters: it holds the impostor accusation ("You're that guy I met
   in the cave to the north!"), the thanks after the rescue, and the Kumogiri messenger who gives the route
   ("You'll find Kumogiri Hamlet 2 just beyond the cave north of this village!"). The "north beyond the lake"
   hint for Mito is spoken in Hamlet 2 (`map-0x14EF`), not Hamlet 1: north of Hamlet 1 the land ends at the
   lake on every side (checked, steps 446-450). So the order is Kashima inn, the cave north of Kashima,
   Hamlet 2, Mito.

   Kashima's inn, done (steps 451-470, session now in the inn's bedroom, level 7, HP 53/53, 1012 Ryo, saved
   to TENGAI1 at Kashima's record keeper). Clean: the record keeper and the save screen again (the slot list
   showed the old save as "Tsukuba Lv 6"), the stay ("It's 10 Ryo for the night. / Will you stay?", "Please
   rest well.", "Take care of yourself, Lord Ziria."), the guest's thanks ("Thank you for rescuing our sacred
   White Deer."), the Kumogiri messenger ("Ziria! I'm from Kumogiri Hamlet! / Chief Kumogiri is waiting for
   you in Kumogiri Hamlet 2.", "You'll find Kumogiri Hamlet 2 just beyond the cave north of this village!"),
   and the accuser by the beds ("Ah! You're that guy I met in the cave to the north!", "Give me back my money!
   / I have a wife and two kids to feed!", "Where do you think you're going?! / Give me my money! / You thief!
   You criminal!"). Inn layout: the record keeper stands in the entrance room, the innkeeper is behind the
   counter on the raised floor (talk across it), the guests are reached through the opening at the back and
   the corridor to the right. Not seen in the inn: `map-0x1447-0x165` (the apology after the impostor is
   exposed) and `0x1BD` (the Cult of Daimon line), which need other story states. One emulator launch failed
   here ("debugger port never opened", session unchanged); the retry worked, and the hung process had to be
   killed by hand.

   Tanuki Cave (`map-0x14D3`), story lines done (steps 471-510, session now in front of the forgiven Odanuki
   by the ladder at the cave's north end, 1124 Ryo). Route: out of Kashima by the south path, on the overworld
   one tile up, five left, then north along the west shore; the cave mouth sits between four trees under the
   mountains. Clean: the location window "Tanuki Cave", the four impostors, each opening with "Ponpokorin!"
   and a full-width portrait ("I am Bokuden, master of the blade! / Think you can beat me, kid? / Have at
   you!", "I'm Ziria, the Fire Hero! / Wahaha! You scared? / C'mon, show me what you got!", "Hoh hoh hoh! I am
   Komon! / Ziria, how dare you oppose the Cult of Daimon? Prepare to be punished!", "Ziria, you naughty boy!
   / It is I, the Toad Hermit!! / You cannot defeat your master!"), the fights ("Defeated Tanuki Bokuden!",
   "Ziria obtained 8 Ryo.", "Acquired 8 Virtue!"), the boss ("You're not going anywhere! / Lord Gomon of Mito
   will give me the lands of Tsukuba once I beat you!", "Odanuki took 63 damage!", "Defeated Odanuki!"), and
   the scene after it: the apology, the Yes/No prompt, the No answer ("You're supposed to be a hero, brave and
   kind! You must forgive me! Sob sob!", then the prompt again), the Yes answer ("Bleeeh! Fooled ya! / See
   you, moron! Ponpokorin!") and "You forgave the Odanuki." Also seen: the item submenu (Use / Give / Drop),
   "Ziria used the Toad Oil!", "Ziria recovered 30 HP!". The cave is a maze of tanuki statues; after each
   impostor falls the hero is moved further in. The session is poked again: the Odanuki beats a level-7 hero
   (HP 48 to 12 in two rounds), so HP and max HP were set to 999 and Attack to 200 in the state of step 501.
   Not done in the cave: its caskets (Toad Oil, 50 Ryo, an empty one).

   Kumogiri Hamlet 2 (`map-0x14EF`, inn `map-0x150B`), part done (steps 511-534, session now in the inn
   beside the hearth, stats still poked). Route: the ladder behind the Odanuki comes out north of the
   mountains; straight north, over the bridge, the hut is the hamlet. Clean: two villagers outside ("Ziria,
   this is Kumogiri Hamlet 2. / Chief Kumogiri is waiting for you inside the inn.", and the three scrolling
   pages starting "Chief Kumogiri founded Kumogiri Hamlets all over the country as beacons of justice,"), and
   everything in the inn: the record keeper at the counter (the prompt, the No answer, "Come back anytime!"),
   the innkeeper, who is the man in blue at the hearth ("Welcome to the inn!", "It's 5 Ryo for the night. /
   Will you stay?", "Please rest well.", "Take care of yourself, Lord Ziria."), the man on the left (three
   pages, "You were probably too young to remember, but..."), the man on the right ("Chief Kumogiri ordered me
   to infiltrate Castle Mito. I just got back. / Apparently, there's a secret path to the lands of Banmo under
   the castle."), and Chief Kumogiri, the old man at the head of the hearth: full-width portrait, six pages
   from "Here you are, Ziria! / It's me, Kumogiri! / You've really grown!" to "Allow me to teach you a
   technique of my own design. / You can use it in battle!", then "Ziria has learned how to steal!". His text
   prints slowly: allow 400 frames a page. Not saved here (the stats are poked).

   Hamlet 2, rest of the outdoors, the store and the Thieving School, done (steps 535-562, session now in
   the school beside the instructor, 1119 Ryo). Clean: the general store (`map-0x1543`: "Welcome, welcome! /
   This is my general store. / Tell me what you need!", Buy Wares / Sell Belongings, the list Toad Oil 18,
   White Toad Oil 52, White Snake Stone 250, White Crane Plume 60, "Have a nice day."), three more villagers
   ("It seems the Cult of Daimon is gathering believers by telling them that if they join, they can become
   immortal.", "The Daimonists are using Mito Town as their base. It's just north from here, beyond the
   lake. / Everyone there has been acting weird ever since!", and, with a small portrait window, "Lord Komon
   was kicked out of Mito Castle by Gomon, one of the heads of the Cult of Daimon! / He's a violent man who
   loves torturing people!"), and the Thieving School (`map-0x155F`, the left of the two southern houses):
   the doorman ("If you can steal the money successfully, you get to keep it for yourself! / Think of it as
   a game and have fun! / But don't forget your quest to defeat Masakado!") and the instructor ("This is a
   Thieving School, where you can improve your thievery in order to help defeat the Cult of Daimon! / Head
   inside, avoid the instructors, and steal the money from the casket!"). How-to: the store keeper is talked
   to from the counter row one tile left of the steps; the school's instructor cannot be reached across his
   table, stand on the raised floor beside him. Villagers wander and block the gap between the southern
   houses; go round. Not seen (other story states): `map-0x14EF-0x2C7` ("Mito Town is finally back to
   normal.") and `0x3E7`. 

   Hamlet 2's Gambling Den (`map-0x1527`, the right-hand southern house; dice text in `script_shop.csv`),
   done (steps 563-594, session now in the den below the gambler in red, 1139 Ryo). Clean: the three
   gamblers ("It's a simple game! / Just bet whether the sum of the two dice will be even or odd!", "The
   dice lady is a real babe! / When I play, I'm not exactly looking at the dice, if you catch my drift!",
   "My, if it isn't Ziria! / Should you really be here? / Eh, I guess it's fine every once in a while!") and
   the whole dice game, three rounds: the panel "Funds 1119両 / Bet 0両" beside the dice lady's portrait (both
   figures are blank until the first Yes), "A single bet is 10 Ryo! / You can bet up to 100 Ryo! Are you
   in?", "Let's start with a 10 Ryo bet!", "Real men risk it all! / How about betting more?" (Yes raises
   the bet by 10), "The dice have been rolled! / So, what will be under the cup? / Will it be even? Or will
   it be odd?", the Even / Odd choice, "The bet is in! / Game on!", the pick shown as "Even" or "Odd" above
   the bet, the result line "6 - 6 : Even", the win ("Luck is on your side, Fire Hero! / How about one more
   game?"), the loss ("If winter comes, can spring be far behind? Let's play one more game!") and the No at
   the first prompt ("No time for games, huh? That's fine! / Come back whenever you feel like it!"). A win
   pays double the bet. After a loss the Bet figure keeps showing 10両 (0両 after a win); a number display,
   not text, not compared with the Japanese build. No at the 10 Ryo prompt just fades out, no line. How-to:
   the dice lady is the woman on the left of the mat, talk from her left; the cushions are solid, so the
   right-hand gamblers are reached along the top row or down the right wall. Not seen: the empty-wallet
   line (`str-0xE1D`). Also in the school: the casket room behind the back door has four instructors and
   the casket in the top row behind racks; one try at it walked back out by the stairs (Check there gives
   "There's nothing out of the ordinary."). Not done: that casket game, the Steal command in a battle.

   Hamlet 2 to Mito, done (steps 595-601, session now just inside Mito Town's east edge with the field menu
   open, level 7, 1139 Ryo, stats still poked). One more Hamlet 2 villager, grey-haired, south-east of the
   houses, has `map-0x14EF-0x3E7` ("Chief Kumogiri has been expecting you, Lord Ziria. / He looks forward
   to teaching you one of the techniques he designed!"), clean; he still says it after the technique is
   learned. Route: leave the hamlet by the east side (between the two stone markers), on the overworld four
   tiles up, five left, north over the second bridge, then north-west to the blue-roofed town. The location
   window reads "Mito Town". 

   Mito Town (`map-0x157B`), part done (steps 602-608, session now on the upper road beside the guard,
   stats still poked). Clean, five townspeople: "I'm glad Komon and his stooges are gone! / I was so sick of
   Kaku's dreadful wordplays!", "The Cult of Daimon is fantastic. It heals all sicknesses, restores your
   youth, and frees you from all the world's ills!", the guard, who wanders the upper road ("No, no, no! Stop
   right there! / Only Daimonists may pass through here! Turn back at once!"), "Our town is peaceful thanks
   to Lord Gomon's protection. / We are eternally grateful.", and "Anyone can become a Daimonist. You simply
   need to go to the church and get baptized. You should go right now!". Layout: the east entrance leads to
   a lower road with an exchange-sign building, a general store and an inn; a road north between them
   reaches an upper road with two more houses and a fenced path going north-east.

   Bug found from the script listing and fixed in `tools/restyle.py`: the amount pattern let a number end
   on a comma, so "両100, but" became "100, Ryo but". Three lines were wrong (Mito's armory
   `map-0x15B3-0x109_4`, "10, Ryo okay?" in `map-0x1BCB`, "1,000, Ryo all right!" at dialogue line 11817);
   they now read "100 Ryo, but", "10 Ryo, okay?", "1,000 Ryo, all right!". No other line changed. Rebuilt
   (sha1 `a9cc6890`), `dist/` regenerated with `tools/release.sh`, identity test and the 47-step replay check
   pass on the new build. The three fixed lines have not been seen in game: session `en2` still runs build
   `babc0728`, whose only difference is those three lines. 

   Mito's buildings, part done (steps 609-632, session now at the inn's counter). Clean: the two houses on
   the upper road (`map-0x15EB`: "Can you believe that the self-proclaimed “Fire Hero” actually thinks he can
   defeat the Cult of Daimon?", then after the box pause "Lord Gomon will surely put an end to him in no
   time!"; `map-0x1607`: "What? You're not a Daimonist? / Leave at once! You're stinking up the place!
   Hmph!"), the warehouse (`map-0x1597`, the exchange-sign building: three pages from "Welcome to the
   warehouse! / Our motto is “Courtesy, kindness, and professionalism”!" to "Get outta here, moron! I hope
   you lose all your stuff!"), the general store (`map-0x163F`: "Welcome to my general store!", "I'll pay
   premium prices if you've got human souls for me!", "See, Lord Gomon pays good money for the souls of
   those with a grudge against the world.") and the inn (`map-0x15CF`: "Huh? You wanna stay? / Sure, I have a
   room, just for you!", "It's 50,000,000 Ryo for the night... / What? You ain't got that much? / Then get
   outta here!"). The curly quotes render. How-to: in the houses and the inn, step onto the raised floor and
   stand below the occupant; Mito's store keeper stands one tile right of Hamlet 2's. Townspeople block the
   road down from the upper road; use the north-south road left of the general store. Not found yet: the
   armory (`map-0x15B3`, which holds the fixed "100 Ryo, but" line). 

   Mito's church (`map-0x1623`), story scene done (steps 633-644, session now on the Odanuki's last page
   after the fight, 1139 Ryo). Route: from the inn's door go right and north, through the gap in the fence
   (three tiles left of where the road meets it), north through the grove; the church is the tall
   blue-roofed building. One more townsperson in the grove: "Those who won't join the Cult of Daimon are
   being “convinced” by Lord Gomon in Mito Castle's dungeons.", clean. In the church: the head priest
   stands behind the lectern (go round it on the right); full-width portrait, "I am the head priest of the
   Daimon church. Are you a faithful believer?" with Yes / No; Yes gives "Hah! Fooled you again! / You're so
   gullible, Ziria! / Ponpokorin!", then "The head priest reveals his true form!" and the Odanuki fight;
   after it "The Daimonists are manipulating youkai and monsters all over the country into doing their
   bidding!", "I'll have the way to the castle opened for you. Please, go to the dungeons and defeat Gomon
   once and for all!", "We'll return to the mountains and cheer for you in secret. Ponpokorin!". All clean.
   Not seen: the No answer (`0x242`).

   Battle menu and Steal, seen in this fight on a first pass that was rewound: the menu reads Attack /
   Jutsu / Item / Steal / Defend / Flee, the battle item list shows six items in the narrow font, Steal
   opens a target list ("Odanuki"), then "Ziria used a thievery technique.", "Ziria stole from Odanuki. /
   Got 54 Ryo." All clean. Not seen: "failed to steal".

   Poke note: something between step 501 and the church put Attack back to 14 while HP stayed 999 (an inn
   stay is the likely cause, not checked). A battle copies the stats when it starts, so poking Attack during
   the fight does nothing: the state of step 640 was poked again (Attack 200) and the scene replayed.

   Mito after the church, part done (steps 645-666, session now in the armory beside its keeper). Every
   townsperson is a tanuki sprite after the fight and they wander fast (step beside one, then talk). Clean:
   the altar tanuki (repeats the two castle pages), the two in the pews ("Ponpokorin! / I'm sorry! I'm
   sorry! / I'll stop tricking people!", "Gomon is holding the townspeople captive in the castle's dungeons.
   / Please, save them!"), three outside ("The Daimonists are stealing the souls of the townspeople and
   using them to revive Masakado!", "I heard Innards Grotto is swarming with the souls of those who can't be
   reborn into this world.", "Gomon has thrown all of the town's residents in the dungeons of Mito
   Castle."), and the armory's keeper ("Go west from Mito Town and head south, and you'll find the mountain
   where our guardian deity, the White Tanuki, lives."). The armory (`map-0x15B3`) is the leftmost building
   on the upper road, sword sign; its keeper walks about behind the table, go round the table on the right.

   A savestate carries the disc data: side session `en3` (a copy of `en2` at step 632 with the new build on
   its memstick) still showed the old "It's usually 100, Ryo but we have a special price of 5,000,000,000
   Ryo for non-members of the Cult of Daimon!" in the armory. So a new build cannot be checked from an old
   session; it needs a boot. That page is the armory keeper's before the church scene (pages: "Welcome to
   the armory!", the Gomon Sword offer, the price, the Gomon doll); the old text wraps cleanly, the new text
   is unseen. The two builds' data tracks differ in 5,556 bytes, not three lines: the text is
   dictionary-coded and the change re-ranked the dictionary, so a byte diff proves nothing either way.
   Check that does work: the `en` route plus `en2`'s presses to step 293, run in one go from boot on each
   build (189,344 frames, 8 minutes each), end on a byte-identical `final.png`. Neither run matches `en2`'s
   own step 293 (a continuous run drifts from a session played state by state), so this compares builds
   with each other, not with the session.

   Side session `en3`, Mito before the church (steps 633-650, old text, left on the lower road). Clean: the
   armory keeper's four pages ("Welcome to the armory!", the Gomon Sword offer, the price page above, "Buy
   now, and I'll throw in a Gomon doll for free! It's a limited edition!") and the town greeter, who roams
   the upper road ("This is Mito Town. / Thanks to the Cult of Daimon, we can all live happy lives."). Nine
   more talks there only repeated lines already seen. Not found in that state: `map-0x157B-0x6C1`, `0x755`,
   `0x7FF`, `0xA28`.

   Mito's west district, part done (`en2` steps 667-682, session now in the second house there, talking to
   its tanuki). Route: from the armory go down to the lower road and west; a long wooden bridge crosses the
   lake to a second group of at least five unsigned houses. Clean: one more tanuki by the armory
   ("Ponpokorin! / Forgive us, Ziria!"), and the first two houses, the pair just north of where the bridge
   lands ("Please save the villagers before you go through Innards Grotto. / Especially the young
   ladies...", "Ponpokorin! / I almost lost my disguise when you were staring at me!"). The tanuki indoors
   move every step; a talk can miss even when adjacent, repeat it.

   More west-district houses (steps 683-721, session now in the north-east house). Clean: `map-0x171F`
   ("Jipang is our home. / Please protect it, Ziria!", the house west of the bridge pair), `map-0x16CB`
   ("Gomon must be waiting for you inside Innards Grotto! / Be careful, Ziria!", north-west house) and
   `map-0x16E7` ("Lord Komon has been driven out of the castle by that Gomon fool. / I hope he's well...",
   north-east house). North of these two a stairway leads up through the rocks. How-to for tanuki that
   keep moving: once one is adjacent, turn to it in its own step, then Circle (opens the field menu) and
   Circle again in a separate step (Talk); pressing Circle right after a move usually misses. Not found
   yet: `map-0x1703-0x141` ("I'm sorry for my harsh words, Ziria.").

   Mito Castle (`map-0x165B`), entered (steps 722-763, session now beside the Iron Key casket, level 8).
   Route: the stairway between the two northern west-district houses (two tanuki at its foot: "Damn those
   Daimonists! / Stick a fork in me 'cause I'm so done with them!"), east across the plateau, up the
   second stairway to the castle gate. Inside: the entrance stairs lead to a wooden hall; its upper-left
   stairs reach a stone floor whose north-east stairs lead to a room with the casket. Clean: random-battle
   text with new enemies (Shikigami, Yako: "Yako used the Mago spell.", "Defeated Yako!"), Flee ("Ziria
   fled.", "Shikigami raced in pursuit."), the level-up run ("Ziria rose to level 8!", "Gained 1 Speed!",
   "HP and TP fully restored! / You're one step closer to bringing down the Cult of Daimon."), and the
   casket ("You look inside the casket. / There is an iron key inside.", "Obtained Iron Key." - shown
   once, with a trailing line break in the script that prints nothing). Pokes: HP 999 and Attack 200 again
   at steps 737 and 741 (the level-up at 741 reset them).

   Iron door and dungeon, part done (steps 764-818, session now upstairs beside the opened door). The door
   is a floor plate in the wooden room reached by the stairs on the stone floor's west side. Check on it:
   "There is an iron door with a 大 symbol painted on it in red. / The door is locked." (the 大 renders as a
   glyph, as at Kashima); Items, Iron Key, Use: "You open the iron door." and a staircase appears beside
   the plate. Below is the dungeon cell crammed with townspeople (`map-0x1693` plus line 1762). Clean so
   far: "Where are we? Who am I? / What are you doing here? / You still have your soul, don't you?", "I'm
   scared! I'm scared! / Gomon snatches your soul the moment you scream during torture!", "What? You're
   gonna fight Gomon? / Hey, it's your funeral!", "Gomon is treating us like cattle... / I'd like him to
   feel our pain one of these days.", "Banmo is beyond Innards Grotto, but good luck getting there with
   Gomon blocking the way!". The crowd moves; talking via the field menu (Circle, then Circle in a new
   step) works reliably. A staircase at the cell's top leads on (to Innards Grotto, by the script).

   More of the cell (steps 819-908): "Take the stairs down and you'll be inside Innards Grotto. Watch out
   for your soul!", "Get out of the way! / This place is cramped enough as it is!", "Gomon will steal your
   soul too... / Just give up and accept your fate!", "Is there no God to help us? / I don't want to lose my
   soul!", "Gomon is down below, inside Innards Grotto. That's where he steals people's souls!", "Let's
   see...Two twos are five! / Three twos are nine! Nine twos are twelve!" (box pause arrow shown), "Don't
   worry about me! / Save the children, I beg you!", "Gomon swaps real people with shapeshifted tanuki to
   take over towns!", and a child's two pages ("They say that you'll become immortal if you join the Cult
   of Daimon, but it's not true!", "It's just a lie they spread to deceive the people of Jipang and take
   over our country! How is everyone so oblivious?!"). All clean. The stairs down are near the cell's top
   left; step 909 stands in Innards Grotto.

   Innards Grotto and Gomon, done (steps 909-1048, session now at the grotto's east stairs after the
   fight, level 8, 1598 Ryo). The location window reads "Innards Grotto". The grotto's floating souls talk
   (`map-0x16AF`): "Urgh...I'm suffering... / Please, deliver me from this pain...", "Masakado consumes the
   souls that end up here...It could be my turn next..."; the other three soul lines (`0x37D`, `0x3D3`,
   `0x47F`) were not caught, the souls drift away. Route: north from the dungeon stairs, west and up the
   winding passage, east along the top, north up the corridor between the two teal pools, then east in the
   last chamber to the stairs; stepping toward them starts Gomon (`script_boss.csv` `boss_0xF005`). Clean:
   the whole intro as scrolling text with his portrait ("Hmph! I see you've made it this far. / Ziria, was
   it? I suppose congratulations are in order!", "I am the first of the Thirteen Daimon Cultists, the Hell
   Magician Gomon! / You don't stand a chance against me!", "You deserve a little boon before your
   death...I will show you my true form!"), "Gomon sprang forward!", "Gomon's attack!", "Multiple
   strikes!", "Gomon took 53 damage!", the win ("Curses! I underestimated you! / But one of my fellow
   cultists will kill you without fail! Just you wait!", "You have defeated Gomon, the first of the
   Thirteen Daimon Cultists! / There are twelve cultists left!"), "Ziria obtained 6 Ryo.", "Acquired 89
   Virtue!". Random battles come every few tiles in the grotto; with base Attack poked they end in one
   round. Battle menu tip: the cursor starts on Attack each round and wraps, so plain Circle attacks; arrow
   presses meant for the map end up moving it. Not seen: Gomon's lose line (`boss_0xF005_lose_1`).

   Banmo, Kumogiri Hamlet 3 (`map-0x19D3`, inn `map-0x19EF`), part done (steps 1049-1101, session now at the
   inn's bedside beside the innkeeper, 1616 Ryo). The grotto's east stairs come out on the overworld north
   of the river (Mito Castle is across it to the south); the hamlet is the hut a few tiles north. First
   battle there: Daimon Acolytes ("Defeated Daimon Acolyte!"). The location window reads "Kumogiri Hamlet
   3". Clean: the greeter ("Lord Ziria! Welcome to the lands of Banmo! This is Kumogiri Hamlet 3!", "The
   Daimonists already have great influence here! Do your best, Lord Ziria!"), and in the inn (the left of
   the two houses north of the three statues): the record keeper's prompt, "Choose where to write the
   file", three guests ("What a weird village that was! / There were only old people there!", "I think it
   was called Ota Village. / You'll find it along the river.", "Maybe the Slug Hermit knows where you can
   find the second Fire Hero!", "He's lived for a long time. I'm sure he knows a thing or two about the Fire
   Clan!"), and the innkeeper by the beds ("Welcome to the inn!", "It's 10 Ryo for the night. / Will you
   stay?", No: the choice echoes as "No", then "Please come again."). Note: presses meant for a talk ran
   into the record keeper's prompt and saved to the session's memstick (`en2` only), with the poked stats.
   Not seen: Komon back in Mito Castle (`map-0x165B-0x378`) and the freed townspeople; both are behind the
   grotto, south of the river.

   More of Hamlet 3 (steps 1102-1132, session now in the general store with the Map of Banmo open, 1602
   Ryo). Clean: the last inn guest, with a portrait window ("My old man told me that the Fire Clan was made
   of three different tribes.", "That must mean there's two other clans besides your own Toad clan,
   Ziria!"), the general store (`map-0x1A0B`, right of the inn: "Welcome, welcome! / This is my general
   store. / Tell me what you need!", the list Toad Oil 18, White Toad Oil 52, White Crane Plume 60, Map of
   Banmo 14, "Map of Banmo, is it?" Yes/No, "Obtained Map of Banmo.", "14 Ryo, please. / Would you like
   anything else?", "Thank you, thank you! / See you soon!"), and "Ziria used the Map of Banmo!". The map
   screen has a red seal with the kanji 磐毛 drawn in the picture, like Tsukuba's 筑波; the map-seal ruling
   covers it (leave it).

   Hamlet 3 villagers (steps 1133-1186). Clean: "The Slug Hermit lives in a small shrine north from
   here!", "According to rumor, the second hero of the Fire Clan is somewhere here in Banmo!", "The three
   Fire Heroes must combine their powers to stand against Masakado!", "You must be Ziria! / Chief Kumogiri
   told us to expect you!", "We're ready to give our lives for you, / Ziria!". The right of the two
   southern houses is a Thieving School with the same doorman line as Hamlet 2's ("If you can steal the
   money successfully, you get to keep it for yourself!"); the left one has a closed wooden door (Check:
   "There's nothing out of the ordinary."); both doors face south. The child by the store, with a
   portrait window: "You won't find anyone stronger than Tsunade around these parts!", "We had a sumo
   tournament recently, and she beat a hundred opponents in a row by ring out!", clean. Not caught:
   `map-0x19D3-0x254` (the kitsune).

   Slug Shrine (`map-0x1A27`), done (steps 1187-1221, session now in the shrine after the scene, 1602 Ryo
   plus one Acolyte fight). Route: leave Hamlet 3 west between the two stone markers, go round the hamlet
   and north; the cave sits on an island in a lake, reached by a bridge. Inside, the passage runs
   north-west to a wooden floor with a hearth; the Slug Hermit sits left of it, talk from below. Clean: the
   full-width scene, nine pages from "Well met, Ziria! / I'm the Slug Hermit. / I've been living here for
   300 years!" to "I've already told Tsunade about you. / Now go, young Ziria!" (including "While she's not
   the brightest girl, she's definitely one of the strongest! / And she's as cute as a button!" and "You'll
   find her at Ashikaga School! / Go meet with her, and stand against the Cult of Daimon together!").

   Shrine to Ota Village (`map-0x1A43`), part done (steps 1222-1298, session now in a north house of Ota,
   level 9, 1726 Ryo). Route: from the shrine's bridge go east to the beach (round the mountains), north
   up the coast, then north-west; a road through a wood leads to the village beside the broken bridge.
   The overworld west of Hamlet 3 is closed by mountains and the river. Clean: new enemies Daimon Bishop
   ("Daimon Bishop used the Mago spell.", "...the Eleca spell.") and Daimonist Kitsune, Kogama joining
   the fight ("Kogama's attack!"), item drops ("Ziria obtained Toad Oil." then "Obtained Toad Oil.",
   "Obtained White Snake Stone."), the level-up to 9 (it reset the poke: HP 999 and Attack 200 poked
   again at step 1249, base byte included). In Ota: "Ota Village used to be a lively, bustling place... /
   But ever since they built that castle on the other side of the river, all of our young'uns have gone
   off to live in town.", the forgetful old man ("Listen. This is a very important tale. / A long time
   ago, Jipang almost fell into... something...", "Because of...Oh, I forget."), "Our priest is looking
   for the Fire Hero! / He said he has something very important to discuss.", the woman with portrait
   ("A powerful young lady called Tsunade chased the Daimonists away from our village.", "If only she
   had come sooner, maybe they wouldn't have destroyed the bridge..."), and the north house (`map-0x1ACF`:
   "All women naturally know a way to send men into panic: crying crocodile tears.", "When Tsunade cries
   crocodile tears, you never know what's going to happen!", "Tsunade is the best wielder of axes in the
   Far East. None can match her skill!", "If you ever find an axe, let Tsunade wield it!").

   Fix: upstream's "going to  happen" had a double space (shown as a wide gap). `restyle.py` now collapses
   runs of spaces between two letters; it touches that line only (menu padding never sits between
   letters). Rebuilt (sha1 `3b8a8289`), `dist/` regenerated, identity test and the 47-step replay check
   pass. Session `en2` still runs the old disc (a savestate carries it), so the fixed line shows only on a
   fresh boot.

   Rest of Ota, done (steps 1299-1391, session now in the inn's bedroom, 1596 Ryo). Layout: the shrine
   (porch, `map-0x2127`) and the sacred tree are on the river at the village's north-west; the armory and
   the warehouse face each other in the middle; the inn (INN sign, `map-0x1A5F`) is on the west side by a
   small bridge. Clean: the villager by the tree ("If we cut down the sacred tree, we could use it as a
   bridge to reach the other side.", "But...It's a sacred tree. We can't just cut it down, right?"), the
   tree's Check ("A rope with evil-warding talismans is wrapped around a large tree.", "This must be the
   sacred tree of the village."), the priest (stand below his table: "I'm the priest of this shrine. / The
   Gods, in all of their mercy, sent me three revelations this morning!", the three revelations about the
   Byakko Axe and "the Fire Hero descendant of the Slug Clan", Yes / No, "Thank you so much. / You truly
   are a Fire Hero!", "You have accepted the priest's request.", "Acquired 71 Virtue!"), the armory (New
   Moon Sword, Shinobi Katabira, Shuriken, Kunai; "New Moon Sword, is it?", "Obtained New Moon Sword.", a
   new message "Unable to hold any more items. / Drop something?" with the item list, "130 Ryo, please.",
   "Thank you very much."), the house south of the armory (`map-0x1AEB`: "According to the old tales, the
   Fire Clan is comprised of multiple clans. / The Toad clan, the Slug clan, and...", "And...and the other
   one! It's the... / The uhm... / Uhhhhhhhhhhhhhh...", "Sorry, I forgot..."), and the whole inn: "Welcome
   to the inn!", "It's 20 Ryo for the night. / Will you stay?", No, "Please come again.", the Kumogiri
   messenger in the back room ("This town's bridge has been destroyed by the Daimonists!", "They've
   finally acknowledged the threat posed by the Fire Heroes.", "The battle is going to be fiercer from now
   on. Hang in there, Ziria!"), the "Yo, yo, yo!" guest (three pages about the hot spring's "blue-eyed
   babe"), and the guest in bed, talked to from above ("Ashikaga School is west of our village. / Its
   library is very well stocked!", "It has books on the Fire Clan and Masakado!"). Casing differs in
   upstream: "Slug Clan" (priest, Ashikaga) and "Slug clan" / "Toad clan" (here, Hamlet 3); not changed.
   Items lost to mashed presses at full-bag prompts: Map of Tsukuba (step 1241) and Giant Tweezers (step
   1334), both already used. Not seen: the priest's No answer (`0x2D2`).

   Ashikaga School (`map-0x1B07`), part done (steps 1392-1468, session now in the west classroom, 1658
   Ryo). Route: leave Ota by its south road; on the overworld follow the dirt road west, then south through
   the wood; the school is the blue-roofed hut among tree stumps (two battles on the way, Daimonist
   Kitsune and Bishops). The menu's location window reads "Ashikaga School". Clean: the hall monitor
   ("Please be quiet! / No running in the hallway!"), the janitor by the Tsunade-shaped hole at the
   hallway's east end ("Just look at this... / Tsunade did it! / I TOLD her not to run in the hallway!"),
   the Lumberjack Village student ("I'm from Lumberjack Village. / To be honest, I really hate
   studying...", "But Mom told everyone I'm a great scholar, so now I'm stuck here!"), the boy standing in
   the hall (four pages, "Made a hole in the floor," to "Why is it ME who has to stand in the hall when
   the one who did all that was Tsunade?!"), and a seated student with a portrait window ("Tsunade ran
   away because she hates studying! She said she wanted to become a lumberjack!"). Talk does not reach
   across the teachers' counters (east room, red figure in an L-shaped counter; west room, the teacher
   behind the lectern); not solved. Not seen: the library menu (`0x4EE` on), the hole's Check line, the
   "Penis" and pants students.

   Lumberjack Village (`map-0x1B23`), Tsunade joined (steps 1469-1539). Route: from the school go south-west
   along the stumps, then west on the road to the hut by the river (four battles on the way, one new line
   "Daimon Acolyte appeared."). The village's entrance is its east side; Tsunade wanders a clearing in the
   tree maze north of the houses, around tile (47,17). Clean: "Lumberjack Village here is always filled
   with the sound of woodchopping." / "...See, what'd I tell you?", and her full-width scene ("I'm Tsunade,
   certified femme fatale! / You're Ziria, right? / I'm a Fire Hero, just like you!", "Let's travel
   together and kick some Daimonist butts! It's gonna be so much fun!", "Oh yeah! I should say goodbye to
   the village elder first!", "Tsunade, the second Fire Hero, / has joined you!").

   Maze tool: the hero's tile X/Y on a field map are at `0x096660A5`/`0x096660A6` (found by RAM diff;
   copies every 0x2C bytes, Kogama's among them). A throwaway BFS (load a play.sh state in one PPSSPP
   process, press each direction 16 frames, read the tile, save a state per new tile) mapped the village's
   1,206 walkable tiles in a few minutes; a shortest path then became one play.sh call. Worth keeping as
   a tool if more mazes come; it is not in the repo.

   Elder and the Byakko Axe, done (steps 1540-1594, session now in the elder's house after the gift).
   Clean: "Acquired 173 Virtue!" closing Tsunade's scene, the two-hero menu header (Ziria Lv 9, Tsunade
   Lv 5) and the Jutsu picker "Ziria / Tsunade", villagers ("The elder is keeping an ancient axe said to
   be able to cut down any tree in a single strike!", "But we can't lift the darn thing! / Not even ten of
   us working together! / What's up with that?", "Tsunade is north of the village, chopping down
   trees!"), the south-west house (`map-0x1B93`, with portrait: "The village elder once mentioned that the
   Byakko Axe was created by someone from the Slug Clan."), and the elder (`map-0x1B77`, portrait: "The
   Slug Hermit entrusted me with the Byakko Axe a long time ago.", "We can't lift it, but I'm sure a
   descendant of the Slug Clan like Tsunade can wield it just fine!", "Take it with you. Go forth, young
   heroes!", "Obtained Byakko Axe. / Who will hold it?" with the Ziria / Tsunade list, "Obtained Byakko
   Axe."). Picking a hero with a full bag gives "Unable to hold any more items. / Drop something?" (seen,
   then undone with `--back 1`; the axe went to Tsunade). Layout: the elder's house is the dark-door house
   north of the inn, entered from tile (51,52); the wooden-door house beside the general store does not
   open ("There's nothing out of the ordinary."). The hero tile address reads other slots after Tsunade
   joined and right after a map change; it settles after a step or two.

   Axe scene and the inn (`map-0x1B3F`), done (steps 1595-1625, session now in the inn's back room beside
   the fortune-teller). Clean: "Acquired 62 Virtue!" after the gift; leaving the elder's house starts a
   full-width scene with Tsunade ("Not even a sacred tree can withstand THIS axe! Hyah!", "(swish)
   (swish)...(slash!) / Tsunade swings her axe and trims Ziria's hair by a few inches!", "Whoops! Sorry
   'bout that, Ziria! / I'm such a klutz! At least I didn't chop your head off, right? Hahaha!"); in the
   inn the record keeper (prompt, No, "Come back anytime!"), the guest in green ("Not even a professional
   lumberjack can cut down a sacred tree with just any old hatchet! You need a special axe for that!") and
   the fortune-teller, four pages from "I'm a fortune-teller! / Let me look into your future..." to
   "...That doesn't sound good, huh?". Upstream's FIXME on that last page (an extra empty box that can
   stick) did not show: one Circle closed it. Layout: the inn is south of the elder's house, door entered
   from the path below; step onto the innkeeper's raised floor through the cushions, take the gap in its
   back wall to the rear corridor, and the guests' room is the right-hand one (enter from its top-right
   gap). Innkeeper's lines not taken (same 20 Ryo lines as Ota's).

   Back to Ota and the sacred tree (`map-0x1A43-0x1B4`), done (steps 1626-1719, session now beside the
   felled tree in Ota, Ziria level 10, Tsunade level 6, 1847 Ryo, pokes worn off). Route from Lumberjack
   Village: out by its east side, east and north-east through the stump forest to the dirt road at Ashikaga
   School (blue hut), follow the road north-east to the river, then east to Ota; in Ota go round the
   warehouse/armory row by the east and take the road above it west to the tree. Clean on the way: the
   first battles with Tsunade (her command menu reads Attack / Jutsu / Item / Cry / Defend; "Tsunade's
   attack!", "Tsunade dodged.", "Daimon Acolyte took 1 damage!" before the axe was equipped), "What will you
   do, Tsunade?", her knockout ("Daimon Bishop used the Eleca spell.", "Tsunade took 12 damage!", "Tsunade
   received deep wounds and became unable to fight.", in red), "Ziria obtained White Snake Stone.", and what
   follows a won battle with a fallen ally: "In preparation for a new battle, Ziria used half his money to
   fully heal all wounds..." and a warp to the last record keeper (Hamlet 3's inn). That run was rewound and
   Tsunade poked instead (HP and max HP 999). Equip for Tsunade: "In hands" (Byakko Axe), "On body", "On
   feet", "Nothing available."; the Map of Banmo again. At the tree, Check repeats the two old lines and
   Talk gives nothing; the scene needs Items, Tsunade, Byakko Axe, Use, standing on the tile below the
   trunk facing up (from the tile right of it, facing left: "Tsunade used the Byakko Axe!" / "But nothing
   happened!"). The scene, full-width picture: "It's my time to shine! I'm gonna chop this tree down in a
   single swing!", "Here goes nothing! / Miso! Ra! MEN!", "The sacred tree falls with a loud “thud,”
   extending to the other side of the river.", "You've formed a makeshift bridge with the sacred tree.",
   "Acquired 164 Virtue!", then both level-ups ("Ziria rose to level 10!", "Gained 1 Defense!", "Gained 2
   Speed!", "Tsunade rose to level 6!", "Gained 2 Attack!", "Gained 2 Defense!", "HP and TP fully
   restored! ..."). One level-up line read "Gained 65347 Attack!": the poke's doing (Attack was 200, the
   new value is lower, and the 16-bit gain wraps), not the port.

   Hawai Village (`map-0x1BAF`, Hot Spring Inn `map-0x1BCB`, Tea House `map-0x1BE7`), done (steps
   1720-1838), and on to Utsunomiya Town (steps 1839-1850, session now just inside the town's south
   entrance, 1835 Ryo, both heroes poked again: HP 999, Ziria's Attack 200, at step 1722). Route: the tree
   bridge is entered by walking north from the trunk tile; on the overworld go north over the next bridge
   to Hawai (palm trees, two ponds). Leaving Hawai, its beach is closed to the west: cross the bridge south,
   go north-west over the plain to a road through the mountain pass, follow it west to the castle. Clean:
   Hawai's greeter with portrait ("These hot springs are fantastic! / Welcome to the hot springs of Hawai
   Village!"), "I heard the lord of Utsunomiya Castle is very young and brave!" (portrait), "You'll feel
   much better if you stay at the inn! Trust me!", "There are dancers at the inn. Their dance is really
   something else! Are they even allowed to show that? Heh heh heh!"; in the inn the free stay ("This is a
   hot spring inn! It's completely free! You should stay for a while! / How about it?", Yes, "Rest well.",
   "See you soon."), three guests ("This hot spring is great! / Makes you forget that whole business about
   Masakado returning!", "Follow the mountains west and you'll get to Utsunomiya Castle.", "The young lord
   of Utsunomiya wants to meet some hero!"), and in the garden behind the back corridor the foreign
   dancers, whose broken English is upstream's on purpose ("We come to Jipang with Hoteimaru!", "Hoteimaru
   search Fire Fighter in Jipang!", "Mount Fuji! Geisha! Sukiyaki! / Shabu-shabu! Tempura! Sushi! / I love
   Jipang!", "Our country full of demon! / Much very scary! / We run to Jipang!", the paid dance as a
   full-width scene, "It's showtime! / Sexy beauty on stage! / Now let's dance!", "Hawaiii, Hawaaaiii! /
   Ziria! / Help friend Hoteimaru!", and the No answer "I know story of man who not spend little money. He
   die alone and sad."). The dance offer showed the old "10, Ryo okay?": this session runs the disc from
   before the comma fix, so this is the known, fixed bug; the fixed line is still unseen in game. Tea
   house: "Welcome to my tea house! / How may I help you?", the list Toad Oil 18, White Toad Oil 52, White
   Snake Stone 250, Antidote 27, "Antidote, is it?", "Obtained Antidote. / Who will hold it?" with the
   Ziria / Tsunade list, "27 Ryo, please.", "Thank you very much." On the road: new enemies Satori
   ("Satori appeared.") and Higitsune ("Higitsune used the Mago spell."). Not seen: the pool's Check line
   (`0xA7`, the pool is closed off by dancers, baskets and trees), the empty-wallet line (`0x5A6`), "There's
   a funny foreigner in Utsunomiya." (`0x389`) and "I heard these hot springs are managed by a group of
   foreigners." (`map-0x1BAF-0xEC`): every villager in the square was talked to, none said it.

   Utsunomiya Town (`map-0x1C3B`) and Castle (`map-0x1CC7`), story done (steps 1851-1967, session now on
   the castle's east walkway after the young lord's request, 1685 Ryo, Lord's Sword held by Ziria). The
   location window reads "Utsunomiya Town". Clean: townspeople ("The brave, young lord of the castle is
   waiting for the arrival of the Fire Heroes.", "Our brave, young lord hates the Cult of Daimon! You're
   not a Daimonist, are you?!", "Are you Ziria? / I heard about you from Hoteimaru, that foreigner near the
   castle!"), two houses ("The young lord of the castle claims to be brave, but I've never actually seen
   him do anything heroic!"; the carpenters, with a portrait, five pages about Tobei, Tamamohime and
   "Shirakawa Castle's trick system"), the warehouse's item side, first seen ("Want to leave something with
   us? / You can store up to 32 items!", "Gotcha! / Will you store anything else?", the closing "Our
   service is nationwide! ..."), the armory (Bandit's Axe 620, Plate Armor 150, Shuriken, Kunai; "Obtained
   Plate Armor. / Who will hold it?", "150 Ryo, please."), the lord's messenger in the north part of town
   (three pages, "You must be Lord Ziria. / I'm a messenger of the brave, young lord of Utsunomiya!" to
   "Please, head to the castle at your earliest convenience!"), Hoteimaru on the terrace below the castle
   (full-width, three pages: "Oh, friend! Ziria! / This is Hoteimaru! Missionary! / Cult of Daimon is cult
   of demons!", "Thirteen demons! / They revive Masakado and end Jipang!", "You are hero! You defeat
   Masakado! / I help! See you soon, byeee!"), two retainers ("Lord Ziria. The truth is...Shirakawa Castle
   has already fallen into the hands of the Daimonists." / "I'm worried about the lord of Shirakawa... / I
   hope he's safe."; "Tamamohime forced Tobei to create a giant trick system in the dungeons of Shirakawa
   Castle." / "Rumor is, once you get lost in those dungeons, you'll never get out again!"), and the young
   lord (full-width portrait: "I am the brave, young lord of Utsunomiya! Tamamohime is an evil Daimonist. /
   Father is in danger!", "...I must ask you to save my father.", Yes / No; No: "I see. That's a shame. / I
   suppose not all heroes are brave..." (rewound); Yes: "I see why they call you a hero! / You truly are
   brave!", "This is the sword Father gave me for my birthday. You may have it!", "You have accepted the
   young lord's request.", "Acquired 143 Virtue!", "Obtained Lord's Sword. / Who will hold it?", and after
   the scene "My father's life is in your hands!"). His text prints slowly: allow 800 frames a page. Route:
   from the town's south entrance the road runs west past a house and the warehouse; north of them the
   armory and a house; the long road north (the messenger stands on it) ends at steps up to a terrace
   (Hoteimaru), and more steps lead to the castle; its throne room is straight up, the lord inside the
   inner dais, entered through the gap in its south side. Not seen: the town's Hoteimaru song, the Tobei
   villager, `0x1E5`, `0x358`, `0x5C8`, `0x765`, and the castle's lines `0xD1`, `0x1B4`, `0x24B`, `0x29F`,
   `0x5B9` (some only after Shirakawa).

   Kumogiri Hamlet 4 (`map-0x1D37`) and the Abukuma Caves (`map-0x1DA7`), part done (steps 1968-2083,
   session now in a Bog Creature battle on the cave's first floor, west of the entrance). Clean: leaving
   Utsunomiya by the south exit starts a full-width Tsunade scene ("Hey, Ziria! / That guy had a weird
   name, huh? / Sounded kinda made-up!", "What was it again? / Hotty-maru? Otter-maru?", "Oh yeah!
   Hotel-maru! / What a funny name!"); Tsunade's level-up to 7 on the road (HP poked again at step 2009).
   Route: from Utsunomiya Castle the overworld road loops round it to the north, along the lake's south and
   east shores, then north; the hamlet is the hut south-east of a cave mouth, the cave is north-west of the
   hamlet (leave the hamlet west, between the two stone markers, then north). Hamlet 4 clean: the location
   window, the villager between the southern houses (two pages, "Those who went inside the Abukuma Caves to
   rescue Tobei came back looking pale as ghosts!" / "...one-eyed monsters! / They're no place for poor
   Tobei!"), the one east of the statues ("I saw the carpenter Tobei being dragged inside the Abukuma Caves
   to the north!"), a guest in the general store (top right: "Lord Ziria! There are creatures nearby that
   can spew poison from their mouths.", "You should stock up on antidotes before you venture forth!"), and
   the Kumogiri informant west of the inn (three pages, "Ziria! I've been waiting for you! / I have new
   intel on the Cult of Daimon!" to "Alas, Shirakawa Castle has been turned into a den of evil!"). Cave
   clean: the location window "Abukuma Caves", Tsunade's line one step in, full-width ("Oh my, Ziria!
   What's the big idea, bringing me out to this deserted place? / You gonna make a move on me?"), the new
   enemy ("Bog Creature sprang forward!", "Bog Creature's attack!", "Multiple strikes!"), and the casket
   south-west of the entrance ("You look inside the casket. / There is toad oil inside.", "Obtained Toad
   Oil. / Who will hold it?", "Obtained Toad Oil."). The green patches are bogs: walking into one leaves
   the hero frozen in a walking state (seen in a test run, not in the session). Not seen yet: Tobei
   (`map-0x1DC3-0x3DD`, a lower floor), the Scroll of Raiko (`map-0x1DDF`), and the inn and the old-lord
   lines of Hamlet 4.

   Hero tile with three in the party: X/Y at `0x096660D1`/`0x096660D2`, mirrored at `0x096660E3`; the old
   `0x096660A5` is then a follower's slot. `tools/poke.py` can now be imported (its `main()` is guarded).

   Next (in `en2`): finish the battle, find the cave's way down to Tobei, then Inugami Village (west) for
   Tobei's Plans and Shirakawa Castle.
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
max HP `+8`, max TP `+A`, level `+C`, Virtue `+D` (3 bytes). Base Attack `+13`, base Defense `+15`, base
Speed `+17` (one byte each); the shown Attack `+1A`, Defense `+1C`, Speed `+1E` are base plus equipment and
get recomputed (on level-up and other events), so poke the base byte too or the boost wears off. Tsunade's
block, same layout, is the next one at `0x09666818` (HP `0x0966681C`, max HP `0x09666820`). Money at `0x09666838`. Level 2 needs 8 Virtue. To use it in a
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
