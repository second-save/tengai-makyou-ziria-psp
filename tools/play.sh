#!/bin/sh
# Frame-exact play on the headless PPSSPP fork: tools/play.sh SESSION [play.py args]. New session: tools/play.sh new NAME [orig]
cd "$(dirname "$0")/.."
export PPSSPP_HEADLESS="${PPSSPP_HEADLESS:-$HOME/develop/tengai-makyou-collection-psp/tools/ppsspp-headless/src/build/PPSSPPHeadless}"
PLAY="$(tools/venv/bin/python tools/skill.py)/scripts/play.py"
if [ "$1" = new ]; then
  s="work/play/$2"; src=build; [ "$3" = orig ] && src=rom
  rm -rf "$s"; mkdir -p "$s/memstick/PSP/GAME"; cp -R "$src/NPJJ30029" "$s/memstick/PSP/GAME/"
  exec tools/venv/bin/python "$PLAY" "$s" --rom "$(ls rom/*.iso)" --sav tools/fixtures/SAVEDATA --wait 900
fi
s="work/play/$1"; shift
exec tools/venv/bin/python "$PLAY" "$s" "$@"
