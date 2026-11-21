#!/bin/bash
# Patches + zip from the current build (tools/build.py), each re-applied and compared:
#   dist/ziria-psn-en.xdelta      CONTENT.DAT (the game and the manual pages)
#   dist/ziria-psn-en-iso.xdelta  the ISO (the emulator's prompts and menus, XMB title and picture)
#   dist/ziria-psn-en.zip         both patches + README.md
# Fails if README.md does not name both built files' sha1. Publishes nothing.
set -o errexit -o pipefail
cd "$(dirname "$0")/.."
shasum -c rom.sha1
mkdir -p dist
patch() {   # original built out
  local sha; sha=$(shasum "$2" | cut -d' ' -f1)
  grep -q "$sha" README.md || { echo "README.md does not list the patched sha1 $sha ($2)"; exit 1; }
  xdelta3 -e -f -9 -B "$(stat -f %z "$1")" -s "$1" "$2" "$3"
  xdelta3 -d -c -s "$1" "$3" | cmp - "$2"
  echo "patched sha1 $sha  $2"
}
patch rom/NPJJ30029/CONTENT.DAT build/NPJJ30029/CONTENT.DAT dist/ziria-psn-en.xdelta
patch rom/*.iso build/ziria_en.iso dist/ziria-psn-en-iso.xdelta
rm -f dist/ziria-psn-en.zip
zip -j -q dist/ziria-psn-en.zip dist/ziria-psn-en.xdelta dist/ziria-psn-en-iso.xdelta README.md
ls -l dist/ziria-psn-en.xdelta dist/ziria-psn-en-iso.xdelta dist/ziria-psn-en.zip
