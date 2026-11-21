"""The 18 manual pages (psp_001..018.png in CONTENT.DAT) redrawn in English.

    manual.py SRC_DIR OUT_DIR [PAGE..]   SRC_DIR: the original PNGs (work/content); writes OUT_DIR/psp_NNN.png and
                                         OUT_DIR/cmp_NNN.png (original above, English below) for review

Each page is a list of steps: C(box) clears a box (each row filled with its most common colour, which keeps
flat panels and vertical gradients), V(box) blends the rows above and below it (horizontal gradients),
T(x, y, text, ...) draws text (x left, y the middle of the first line;
with w= it wraps, lh is the line pitch), P(box, x, y) pastes a piece of the original page (icons).
Fonts: M+ 1p (fonts/, SIL OFL). Names and terms follow the game's English script (LIPEMCO + our rulings)."""
import io, os, sys
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = {False: os.path.join(ROOT, 'fonts', 'MPLUS1p-Regular.ttf'), True: os.path.join(ROOT, 'fonts', 'MPLUS1p-Bold.ttf')}
INK, WHITE, ORANGE = (63, 58, 57), (255, 255, 255), (238, 120, 0)


def C(x0, y0, x1, y1):
    return ('C', (x0, y0, x1, y1))


def V(x0, y0, x1, y1):
    return ('V', (x0, y0, x1, y1))


def P(x0, y0, x1, y1, x, y):
    return ('P', (x0, y0, x1, y1, x, y))


def T(x, y, text, size=11, bold=False, color=INK, w=None, lh=None, align='l', fit=None):
    return ('T', (x, y, text, size, bold, color, w, lh or size + 5, align, fit))


def font(size, bold):
    return ImageFont.truetype(FONT[bold], size)


def wrap(text, f, w):
    lines = []
    for para in text.split('\n'):
        line = ''
        for word in para.split(' '):
            cand = (line + ' ' + word) if line else word
            if w and line and f.getlength(cand) > w:
                lines.append(line); line = word
            else:
                line = cand
        lines.append(line)
    return lines


def render(im, steps):
    orig = im.copy()
    px = im.load()
    d = ImageDraw.Draw(im)
    for kind, a in steps:
        if kind == 'C':
            x0, y0, x1, y1 = a
            for y in range(y0, y1):   # the colour just left and right of the box, row by row
                c = Counter(px[x, y] for x in (x0 - 2, x0 - 1, x1, x1 + 1)).most_common(1)[0][0]
                for x in range(x0, x1): px[x, y] = c
        elif kind == 'V':
            x0, y0, x1, y1 = a
            for x in range(x0, x1):   # blend the pixel above the box into the one below, column by column
                top, bot = px[x, y0 - 1], px[x, y1]
                for y in range(y0, y1):
                    t = (y - y0 + 1) / (y1 - y0 + 1)
                    px[x, y] = tuple(round(u + (v - u) * t) for u, v in zip(top, bot))
        elif kind == 'P':
            x0, y0, x1, y1, x, y = a
            im.paste(orig.crop((x0, y0, x1, y1)), (x, y))
        else:
            x, y, text, size, bold, color, w, lh, align, fit = a
            f = font(size, bold)
            while fit and f.getlength(text) > fit:   # one line that must fit: shrink the font
                size -= 1; f = font(size, bold)
            for i, line in enumerate(wrap(text, f, w)):
                dx = {'l': 0, 'c': ((w or 0) - f.getlength(line)) / 2, 'r': (w or 0) - f.getlength(line)}[align]
                assert not w or f.getlength(line) <= w + 0.5, 'too wide: %r' % line
                d.text((x + dx, y + i * lh), line, font=f, fill=color, anchor='lm')
    return im


def boxes(tops, head, body, rows):
    """Pages 14-16: two columns of boxes (left x 18-235, right 245-462), each a gray header (name, target and
    cost) over a white description. tops: the boxes' top border rows; rows: left column first."""
    out = []
    for k, (name, cost, what) in enumerate(rows):
        x0 = 18 if k < len(tops) else 245
        t = tops[k % len(tops)]
        hy, by = t + 1 + head / 2, t + head + 1 + body / 2   # middle of the header and of the description
        out += [C(x0 + 2, t + 2, x0 + 215, t + head), T(x0 + 4, hy, name, 10, True, WHITE)]
        if cost:
            out.append(T(x0 + 100, hy, cost, 9, True, WHITE, w=113, align='r'))
        out += [C(x0 + 4, t + head + 2, x0 + 212, t + head + body - 1), T(x0 + 6, by, what, 10, True, fit=204)]
    return out


TITLE = 'Tengai Makyo ZIRIA'
PAGES = {
    1: [C(60, 33, 158, 47), T(62, 40, 'PC Engine Archives', 10, True, WHITE),
        C(68, 208, 118, 234), T(43, 220, 'Manual', 17, True, WHITE, w=100, align='c'),
        C(216, 22, 400, 44), T(220, 33, TITLE, 18, True),
        C(208, 58, 470, 98), T(210, 66, 'The first entry in the great RPG series "Tengai Makyo": young Ziria, last of the '
                                        'Fire Clan, and his companions set out on an adventure.', 11, True, w=258, lh=14),
        C(296, 122, 370, 138), T(300, 130, 'Game info', 11, True, w=64, align='c'),
        C(216, 140, 309, 238), C(318, 140, 462, 157), C(350, 158, 462, 190), C(318, 190, 462, 238),
        T(220, 147, 'Genre', 11, True), T(328, 147, 'Role-playing', 11, True),
        T(220, 171, 'Players', 11, True), T(352, 163, '1', 11, True), T(352, 178, '1', 11, True),
        T(220, 195, 'System', 11, True), T(328, 195, 'PC Engine (CD-ROM²)', 11, True),
        T(220, 211, 'Maker', 11, True), T(328, 211, 'Hudson', 11, True),
        T(220, 227, 'First released', 11, True), T(328, 227, 'June 1989', 11, True)],
    2: [C(18, 5, 470, 22), T(20, 14, 'Health precautions', 13, True),
        C(35, 36, 470, 51), T(36, 44, 'WARNING   Seizures caused by flashing lights', 11, True),
        C(18, 54, 470, 106), T(20, 61, 'A few people may have seizures (muscle twitching, convulsions, altered vision, '
                                       'loss of awareness) when exposed to flashing lights or patterns on a screen. If '
                                       'you have ever had such symptoms, see a doctor before playing.', 10, True, w=446, lh=15),
        C(35, 109, 470, 125), T(36, 117, 'CAUTION   Stop playing at once', 11, True),
        C(18, 128, 470, 182), T(20, 135, 'if you feel any of the symptoms above, or a headache, dizziness, nausea, '
                                         'fatigue, motion sickness, or discomfort or pain in your eyes, ears, hands, arms, '
                                         'feet or anywhere else. If it does not go away, see a doctor.',
                                10, True, w=446, lh=15),
        C(33, 184, 470, 242),
        T(36, 191, 'Play in a well-lit room and stay as far from the screen as you can.', 10, True),
        T(36, 206, 'Do not play when you are tired or short of sleep.', 10, True),
        T(36, 221, 'For your health, take a 15-minute break every hour.', 10, True),
        T(36, 236, 'If you feel unwell while playing, stop at once.', 10, True)],
    3: [C(18, 8, 200, 25), T(20, 17, 'Precautions', 13, True),
        C(35, 44, 470, 59), T(37, 52, 'This software is for PSP® (PlayStation®Portable) only.', 11, True),
        C(35, 68, 470, 101), T(37, 76, 'Always update the system software of your PSP® (PlayStation®Portable) to the '
                                       'latest version before use.', 11, True, w=425, lh=18)],
    4: [C(16, 10, 470, 26), T(18, 17, 'Playing on PSP® (PlayStation®Portable) ①', 15, True),
        V(14, 41, 468, 55), T(18, 48, 'When playing this title on PSP®, please note:', 11, True),
        C(35, 62, 470, 74), T(37, 68, 'PSP® (PlayStation®Portable) peripherals are not supported.', 10, True),
        V(14, 112, 468, 126), T(18, 119, 'About the System Menu', 11, True),
        C(22, 131, 470, 178), T(24, 138, 'Press the', 10, True), P(69, 133, 87, 144, 73, 133),
        T(95, 138, 'button during play to open the System Menu.', 10, True),
        T(24, 155, 'There you can read the "Manual", use "Save (Suspend)" and "Load (Resume)", change the '
                   '"Screen Size" and turn the "Autosave" of the Backup RAM data on or off.', 10, True, w=436, lh=16)],
    5: [C(16, 10, 470, 26), T(18, 17, 'Playing on PSP® (PlayStation®Portable) ②', 15, True),
        V(14, 41, 468, 55), T(18, 48, 'Soft reset', 11, True),
        C(22, 60, 470, 90), T(24, 67, 'In this title, hold the START button and press SELECT during play to reset the '
                                      'game.', 10, True, w=436, lh=16),
        C(42, 98, 425, 112), T(44, 105, 'A soft reset does not save your progress.', 10, True),
        V(14, 136, 468, 150), T(18, 143, 'Rapid fire', 11, True),
        C(22, 155, 470, 169), T(24, 162, 'This title has rapid fire. The buttons are:', 10, True),
        V(40, 178, 82, 196), T(41, 187, 'button', 12, True), V(40, 205, 82, 223), T(41, 214, 'button', 12, True),
        C(104, 178, 206, 196), T(106, 187, 'rapid fire', 12, True),
        C(104, 205, 206, 223), T(106, 214, 'rapid fire', 12, True)],
    6: [C(16, 10, 470, 26), T(18, 18, 'Button names in the game', 15, True),
        C(22, 33, 470, 76), T(24, 40, 'PC Engine Archives recreate PC Engine titles of the past, so the game may show '
                                      'the button names of the PC Engine pad (controller). The PSP® '
                                      '(PlayStation®Portable) buttons match them as shown below.', 10, True, w=436, lh=15),
        V(14, 85, 300, 97), T(18, 91, 'Button chart', 11, True)]
       + [s for y, top, low in ((116, 'START button', 'RUN button'), (184, 'SELECT button', 'SELECT button'))
          for s in (C(15, y - 7, 108, y + 8), T(15, y, top, 12, True, WHITE, w=93, align='c'),
                    V(15, y + 16, 108, y + 30), T(15, y + 23, low, 12, True, w=93, align='c'),
                    V(15, y + 33, 108, y + 43), T(15, y + 38, 'In-game name', 10, True, WHITE, w=93, align='c'))]
       + [s for y, low in ((116, 'I button'), (184, 'II button'))
          for s in (C(412, y - 7, 463, y + 8), T(414, y, 'button', 12, True, WHITE),
                    V(382, y + 16, 463, y + 30), T(382, y + 23, low, 12, True, w=81, align='c'),
                    V(382, y + 33, 463, y + 43), T(382, y + 38, 'In-game name', 10, True, WHITE, w=81, align='c'))],
    7: [C(16, 10, 470, 26), T(18, 18, 'Saving (suspend save)', 15, True),
        C(16, 34, 338, 80), T(18, 41, 'This game is listed under "Memory Stick™" or "System Storage" in the "Game" '
                                      'column, but its save data is kept in "Saved Data Utility".', 10, True, w=310, lh=16),
        C(16, 89, 338, 119), T(18, 96, 'You can save your settings and progress as save data, up to 5 files. Save '
                                       'from the System Menu.', 10, True, w=310, lh=16),
        V(370, 73, 392, 82), T(368, 77, 'Game', 7, True, WHITE, w=26, align='c'),
        V(394, 90, 456, 101), T(396, 93, 'Saved Data\nUtility', 7, True, WHITE, lh=8),
        C(45, 151, 446, 213),
        T(46, 158, 'Each save file needs about 1000KB of free space on the storage media.', 10, True),
        T(46, 174, 'Save data made on PSP® cannot be used on PlayStation®3, and save data made on '
                   'PlayStation®3 cannot be used on PSP®.', 10, True, w=398, lh=16),
        T(46, 206, 'Only Backup RAM data can be exchanged with PlayStation®3.', 10, True)],
    9: [C(16, 10, 200, 26), T(18, 18, 'Controls ②', 15, True),
        C(167, 42, 300, 53), T(170, 47, 'Dash', 11, True, WHITE),
        C(168, 57, 402, 87), P(170, 58, 182, 70, 170, 58),
        T(184, 64, 'Hold the button while you move with the', 10, True), T(172, 80, 'D-pad to go faster.', 10, True),
        C(167, 142, 300, 153), T(170, 147, 'Auto battle', 11, True, WHITE),
        C(168, 157, 402, 220), P(182, 206, 193, 218, 182, 206),
        T(172, 164, 'Press the SELECT button in battle to fight', 10, True),
        T(172, 180, 'automatically.', 10, True),
        T(172, 196, '* Only the "Attack" command is used.', 10, True),
        T(196, 212, 'Press the button to stop.', 10, True)],
    10: [C(16, 10, 300, 26), T(18, 18, 'Starting the game', 15, True),
         C(165, 33, 466, 238),
         T(168, 42, 'Press the', 10, True), P(244, 37, 256, 47, 218, 37),
         T(233, 42, 'button or the START button on the title', 10, True), T(168, 57, 'screen.', 10, True),
         T(168, 76, '■ Start', 11, True, ORANGE),
         T(168, 92, 'Starts the game. To play from the beginning, choose the file marked "New Game". '
                    'To continue, choose the file to load.', 10, True, w=294, lh=15),
         T(168, 142, '■ Copy', 11, True, ORANGE),
         T(168, 158, 'Copies save data. Choose a file, then where to copy it.', 10, True, w=294, lh=15),
         T(168, 178, '■ Erase', 11, True, ORANGE),
         T(168, 194, 'Erases save data.', 10, True),
         T(168, 209, '* Erased data cannot be recovered.', 10, True)],
    11: [C(16, 10, 300, 26), T(18, 18, 'How to play', 15, True),
         C(16, 34, 334, 228),
         T(20, 41, 'After the opening, the game starts at the Toad Hermit\'s house on Mount Tsukuba. Talk to the '
                   'toad by the house for travel money, then buy weapons and items in Tsukuba Village. The Daimon '
                   'Church, which plots Masakado\'s revival, torments the towns and villages on your way. Help the '
                   'people as you cross Jipang, and seek your Fire Clan companions.', 10, True, w=310, lh=15),
         T(20, 146, 'Defeat monsters to gain levels, and spend the money you earn on better equipment. If your '
                    'HP drops to zero in battle, you return to the inn of the town where you last saved, with half '
                    'your money. When your HP runs low, rest before going on.', 10, True, w=310, lh=15)],
    12: [C(16, 10, 300, 26), T(18, 18, 'The screen', 15, True),
         V(232, 44, 468, 58), T(234, 51, 'What the screen shows', 11, True),
         C(250, 62, 468, 78), T(252, 70, 'Name / Level / HP / TP', 11, True),
         C(250, 80, 468, 96), T(252, 88, 'Location / Money (Ryo)', 11, True),
         C(250, 99, 288, 113), T(252, 106, 'Menu', 11, True)]
        + [s for k, (cmd, what) in enumerate((('Talk', 'Talk to people'), ('Items', 'Use / give / drop items'),
                                              ('Jutsu', 'Cast jutsu, give scrolls'), ('Status', 'Show all stats'),
                                              ('Kogama', 'Warp to a hamlet'), ('Equip', 'Equip / remove gear'),
                                              ('Check', 'Look one step ahead'), ('Mode', 'Help, settings, etc.')))
           for s in (C(292, 102 + 16 * k, 329, 117 + 16 * k), T(291, 109 + 16 * k, cmd, 9, True, WHITE, w=40, align='c'),
                     C(335, 102 + 16 * k, 454, 117 + 16 * k), T(337, 109 + 16 * k, what, 9, True))],
    13: [C(16, 10, 300, 26), T(18, 18, 'Battle commands', 15, True)]
        + [s for top, bot, cut, cmd, what in (
            (42, 62, 216, 'Attack', 'Attack with your equipped weapon.'),
            (71, 91, 216, 'Item', 'Use items to heal or to attack.'),
            (100, 120, 216, 'Defend', 'Guard to take less damage.'),
            (129, 149, 216, 'Jutsu', 'Use jutsu to attack or heal.'),
            (158, 192, 259, 'Steal / Cry /\nFlirt', 'Each hero\'s special move, such\nas stealing money from enemies.'),
            (201, 221, 216, 'Flee', 'Run away from the battle.'))
           for s in (C(168, top + 1, cut - 3, bot), C(cut + 3, top + 2, 450, bot - 1),
                     T(169, (top + bot) / 2 - 7 * cmd.count('\n'), cmd, 10, True, WHITE, lh=14),
                     T(cut + 6, (top + bot) / 2 - 7 * what.count('\n'), what, 10, True, lh=14))],
    14: [C(16, 10, 300, 26), T(18, 18, 'Jutsu ①', 15, True),
         C(16, 34, 466, 63), T(18, 41, 'Help the sacred beasts you meet on your journey and they give you jutsu '
                                       'scrolls. Jutsu cost TP to use.', 10, True, w=444, lh=16),
         C(16, 68, 200, 80), T(18, 74, "■ Ziria's jutsu", 11, True, ORANGE),
         C(260, 223, 466, 235), T(266, 229, '* Ziria can learn 24 jutsu in all.', 9, True, w=196, align='r')]
        + boxes((82, 110, 139, 167, 196), 10, 14, (
            ('Wakakusa', '1 ally (TP 2)', 'Restores 50 HP to one ally.'),
            ('Konabi', '1 enemy (TP 2)', 'Fire powder: about 30 damage.'),
            ('Raiko', 'All enemies (TP 3)', 'Lightning: about 20 damage to all.'),
            ('Tsukine', '1 enemy (TP 4)', 'Puts one enemy to sleep.'),
            ('Rakka', '1 enemy (TP 3)', "Halves one enemy's defense."),
            ('Kinin', '1 enemy (TP 3)', "Seals one enemy's jutsu."),
            ('Unkai', '1 enemy (TP 4)', 'Blinds an enemy so its attacks miss.'),
            ('Doromushi', 'All enemies (TP 3)', 'Halves the speed of all enemies.'),
            ('Jinrai', 'All enemies (TP 7)', 'Lightning: about 40 damage to all.'),
            ('Kiyomizu', 'All allies (TP 2)', 'Less damage from poison swamps.'))),
    15: [C(16, 10, 300, 26), T(18, 18, 'Jutsu ②', 15, True),
         C(16, 34, 220, 48), T(18, 41, "■ Orochimaru's jutsu", 11, True, ORANGE)]
        + boxes((50, 86, 122, 158, 194), 15, 16, (
            ('Hyoryu', '1 enemy (TP 15)', 'Icy blast: about 150 damage.'),
            ('Uryu', 'All enemies (TP 16)', 'Icy blast: about 100 damage to all.'),
            ('Toryu', 'All enemies (TP 11)', 'Freezing: about 60 damage to all.'),
            ('Kazahebi', 'All allies (TP 3)', "Doubles the party's speed."),
            ('Hihebi', 'All allies (TP 18)', "Doubles the party's attack."),
            ('Ishihebi', 'All allies (TP 9)', "Doubles the party's defense."),
            ('Harukaze', '1 ally (TP 11)', "Fully restores one ally's HP."),
            ('Hanakabe', 'All allies (TP 10)', "Blocks the enemies' normal attacks."),
            ('Yukidoke', '1 ally (TP 2)', 'Removes jutsu cast on the party.'))),
    16: [C(16, 10, 300, 26), T(18, 18, 'Items', 15, True),
         C(260, 215, 466, 227), T(266, 221, '* There are many other items too.', 9, True, w=196, align='r')]
        + boxes((50, 92, 134, 176), 15, 17, (
            ('Toad Oil', '', 'Restores 30 HP to one ally.'),
            ('Antidote', '', "Cures one ally's poison."),
            ('White Snake Stone', '', 'Restores 8 TP to one ally.'),
            ('Shuriken', '', 'Damages all enemies (in battle).'),
            ('Gunpowder Orb', '', 'Damages all enemies (in battle).'),
            ('White Crane Plume', '', 'Warps to a visited Kumogiri Hamlet.'),
            ('White Pheasant Tail', '', 'Escapes from a cave or dungeon at once.'),
            ('Maps', '', 'Regional maps of Jipang (Tsukuba...).'))),
    17: [C(16, 10, 300, 26), T(18, 18, 'Saving to Backup RAM', 15, True),
         C(16, 34, 466, 64), T(20, 41, 'This title supports Backup RAM. Its data is saved on its own as "Backup RAM '
                                       'data" and can be copied to PlayStation®3 to play there.', 10, True, w=440, lh=16),
         C(35, 75, 450, 106),
         T(36, 82, 'Saving Backup RAM data needs about 200KB of free space on the storage media.', 10, True),
         T(36, 98, 'Ordinary save data does not include the Backup RAM contents.', 10, True),
         V(153, 126, 468, 139), T(156, 132, 'About saving', 11, True),
         C(154, 146, 466, 222),
         T(158, 154, 'Talk to the record keeper at an inn to record your adventure so far. You can keep up to 4 '
                     'files: choose where to save.', 10, True, w=300, lh=16),
         T(158, 202, '* Saving over a file replaces its data.', 10, True)],
    18: [C(130, 9, 350, 24), T(10, 16, 'Contact for this product', 13, True, WHITE, w=460, align='c'),
         V(32, 36, 236, 52), T(34, 44, 'Hudson User Support Center', 12, True),
         C(166, 54, 238, 70), T(168, 63, '(Navi Dial)', 9, True),
         V(32, 74, 242, 90), T(34, 82, 'If you cannot use Navi Dial:', 12, True),
         C(248, 36, 456, 106),
         T(250, 43, '◆ We cannot answer strategy questions.', 9, True),
         T(250, 57, '◆ Hours: 12:00 - 17:30', 9, True),
         T(261, 71, '(except Saturdays, Sundays and holidays)', 9, True),
         T(250, 85, '◆ Please check the number carefully', 9, True),
         T(261, 99, 'before calling.', 9, True),
         C(240, 120, 362, 135), T(243, 128, 'Hudson Soft Co., Ltd.', 12, True),
         C(14, 181, 230, 193), T(15, 187, '"Tengai Makyo" is a registered trademark of Hudson Soft Co., Ltd.', 9, True),
         C(54, 199, 345, 213), T(54, 206, 'is a registered trademark of Hudson Soft Co., Ltd. and NEC BIGLOBE, Ltd.',
                                  9, True),
         C(14, 219, 332, 231), T(15, 225, 'This product uses DynaFont by DynaComware Corp.', 9, True),
         C(14, 231, 250, 243), T(15, 237, 'DynaFont is a registered trademark of DynaComware Taiwan Inc.', 9, True),
         C(405, 229, 468, 244), T(340, 237, 'No unauthorized reproduction', 8, True, w=126, align='r')],
    8: [C(16, 10, 200, 26), T(18, 18, 'Controls ①', 15, True),
        C(20, 42, 103, 56), T(18, 49, 'D-pad', 12, True, WHITE, w=86, align='c'),
        C(20, 60, 102, 89), T(22, 68, 'Move /\nChoose command', 10, True, ORANGE, lh=14),
        C(20, 183, 103, 197), T(18, 190, 'Analog pad', 12, True, WHITE, w=86, align='c'),
        C(20, 201, 102, 230), T(22, 209, 'Move /\nChoose command', 10, True, ORANGE, lh=14),
        C(167, 46, 208, 59), T(168, 52, 'button', 12, True, WHITE),
        C(169, 198, 260, 212), T(167, 205, 'SELECT button', 12, True, WHITE, w=95, align='c'),
        C(169, 215, 260, 230), T(167, 223, 'Auto battle', 11, True, ORANGE, w=95, align='c'),
        C(302, 198, 389, 212), T(300, 205, 'START button', 12, True, WHITE, w=91, align='c'),
        C(302, 215, 389, 230), T(300, 223, 'Start', 11, True, ORANGE, w=91, align='c'),
        C(389, 44, 432, 56), T(391, 50, 'button', 12, True, WHITE), C(389, 64, 432, 76), T(391, 70, 'button', 12, True, WHITE),
        C(401, 86, 458, 99), T(403, 92, 'button', 12, True, WHITE), C(401, 140, 458, 153), T(403, 146, 'button', 12, True, WHITE),
        C(363, 104, 458, 131), T(368, 111, 'Confirm /\nOpen commands', 10, True, ORANGE, lh=14),
        C(363, 158, 458, 185), T(368, 165, 'Cancel /\nClose commands', 10, True, ORANGE, lh=14)],
}


def page(p, png):
    """Original page p as PNG bytes -> the English page as PNG bytes (tools/build.py)."""
    im = render(Image.open(io.BytesIO(png)).convert('RGB'), PAGES[p])
    b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
    return b.getvalue()


def main():
    src, out = sys.argv[1], sys.argv[2]
    pages = [int(p) for p in sys.argv[3:]] or sorted(PAGES)
    os.makedirs(out, exist_ok=True)
    for p in pages:
        name = 'psp_%03d.png' % p
        orig = Image.open(os.path.join(src, name)).convert('RGB')
        new = render(orig.copy(), PAGES[p])
        new.save(os.path.join(out, name))
        cmp = Image.new('RGB', (orig.width, orig.height * 2 + 4), (255, 0, 255))
        cmp.paste(orig, (0, 0)); cmp.paste(new, (0, orig.height + 4))
        cmp.save(os.path.join(out, 'cmp_%03d.png' % p))


if __name__ == '__main__':
    main()
