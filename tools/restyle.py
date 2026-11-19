"""Apply this project's style rulings to LIPEMCO's English script (docs/decisions.md, glossary.md):
no honorifics, shorter names (long vowels dropped), money written "Ryo".

    restyle.py SRC_SCRIPT_DIR DST_SCRIPT_DIR     writes every script_*.csv; only the English column changes

Only the translation column (6th) of `string` rows is edited. script_credits.csv is copied as is (real people's
names). Every rule is length-neutral or shorter, except money(): upstream writes the kanji as a currency sign
("両20"), we spell it out ("20 Ryo", +3 characters). The build re-wraps lines (tenma_scriptwrap)."""
import csv, os, re, shutil, sys

LADIES = {'Yashahime', 'Tsukihime', 'Tsunade'}
TITLES = {'Priest', 'Hero', 'Brave', 'Lord', 'Lady', 'Master', 'Princess'}   # already a title: just drop -sama
# Hepburn without long vowels. Names only, listed one by one: a blanket ou->o would hit English words.
NAMES = ('Akurou Goumon Danjou Koumon Rikuu Mutekiou Toubei Suioumaru Koufu Genoumaru Banmou Douman Shuusaku Kyuubi '
         'Doguu Gouyokku Byakkou Yourou Mouryou Sesshou Juubei Shunkou Kamikouchi Raikou Rakuyou Shinpuu Daisoujou '
         'Fuuma Ginrouki Kongouki Yuunagi Sesshouseki Musou Zenkou Bashou Kyuusa Jakou Yakou Fuurinkazan Fuujin '
         'Tenkuu Hyouryuu Uryuu Touryuu Oodanuki Oota Ookamuro Oogumo').split()


def short(name):
    return re.sub(r'(?i)ou|oo', lambda m: m.group()[0], name).replace('uu', 'u')


NAME_RE = re.compile(r'\b(%s)\b' % '|'.join(sorted(NAMES, key=len, reverse=True)))
SAMA_RE = re.compile(r"(?:\b(\w+) )?\b((?:[A-Z]-)*)([A-Z][\w']*)-sama\b")
DROP_RE = re.compile(r"(?<=\w)-(?:san|chan|kun|dono)\b")
RYO_RE = re.compile(r'\bryo\b')
MONEY_RE = re.compile(r'両(\*\*|\[number\]|\d[\d,]*)')   # ** and [number] are the game's amount placeholders
GLOSS_RE = re.compile(r' \(\d+ ryou\)')   # upstream explains the sign once: "両20 (20 ryou)"


def sama(m):
    prev, stutter, name = m.group(1), m.group(2), m.group(3)
    lead = prev + ' ' if prev else ''
    if prev in TITLES:
        return lead + stutter + name
    title = 'Lady' if name in LADIES else 'Lord'
    return lead + (title[0] + '-') * stutter.count('-') + title + ' ' + name   # "Z-Ziria-sama" -> "L-Lord Ziria"


def restyle(t):
    t = SAMA_RE.sub(sama, t)
    t = DROP_RE.sub('', t)
    t = NAME_RE.sub(lambda m: short(m.group()), t)
    return RYO_RE.sub('Ryo', t)


def money(t):
    return MONEY_RE.sub(r'\1 Ryo', GLOSS_RE.sub('', t))


def selftest():
    for a, b in [("It's 両** for the night.", "It's ** Ryo for the night."), ('両[number], please.', '[number] Ryo, please.'),
                 ('Obtained 両20 (20 ryou).', 'Obtained 20 Ryo.'), ('両1,000 at a time', '1,000 Ryo at a time')]:
        assert money(a) == b, (a, money(a), b)
    for a, b in [('O Masakado-sama, hear us!', 'O Lord Masakado, hear us!'),
                 ('Z-Ziria-sama!', 'L-Lord Ziria!'),
                 ('Priest Ozuno-sama and Yashahime-sama', 'Priest Ozuno and Lady Yashahime'),
                 ('Ziria-san, Osae-chan, Musashi-dono', 'Ziria, Osae, Musashi'),
                 ("Koumon-sama's 50 ryo", "Lord Komon's 50 Ryo"),
                 ('Our Fuurinkazan Sword. You would know, Oodanuki.', 'Our Furinkazan Sword. You would know, Odanuki.')]:
        assert restyle(a) == b, (a, restyle(a), b)
        assert len(restyle(a)) <= len(a), a


def main():
    selftest()
    src, dst = sys.argv[1], sys.argv[2]
    total = 0
    for f in sorted(os.listdir(src)):
        if not re.match(r'script_.*\.csv$', f): continue
        if f == 'script_credits.csv':
            shutil.copy(os.path.join(src, f), os.path.join(dst, f)); continue
        rows = list(csv.reader(open(os.path.join(src, f), encoding='utf-8', newline='')))
        n = 0
        for r in rows:
            if len(r) > 5 and r[0] == 'string':
                new = restyle(r[5])
                assert len(new) <= len(r[5]), (f, r[1])
                new = money(new)
                assert '両' not in new, (f, r[1], new)
                assert not re.search(r'-(sama|san|chan|kun|dono)\b', new), (f, r[1], new)
                n += new != r[5]
                r[5] = new
        with open(os.path.join(dst, f), 'w', encoding='utf-8', newline='') as o:
            csv.writer(o, lineterminator='\n').writerows(rows)
        total += n
        print('%-28s %5d lines changed' % (f, n))
    print('total %d' % total)


if __name__ == '__main__':
    main()
