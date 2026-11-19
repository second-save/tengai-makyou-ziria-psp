#!/bin/bash
# Patch + zip from the current build: dist/ziria-psn-en.xdelta (re-applied and compared), dist/ziria-psn-en.zip
# (patch + README.md only). Fails if README.md does not name the built file's sha1. Publishes nothing.
set -o errexit -o pipefail
cd "$(dirname "$0")/.."
orig=rom/NPJJ30029/CONTENT.DAT; built=build/NPJJ30029/CONTENT.DAT; out=dist/ziria-psn-en
shasum -c rom.sha1
sha=$(shasum "$built" | cut -d' ' -f1)
grep -q "$sha" README.md || { echo "README.md does not list the patched sha1 $sha"; exit 1; }
mkdir -p dist
xdelta3 -e -f -9 -s "$orig" "$built" "$out.xdelta"
xdelta3 -d -c -s "$orig" "$out.xdelta" | cmp - "$built"
rm -f "$out.zip"
zip -j -q "$out.zip" "$out.xdelta" README.md
echo "patched sha1 $sha"; ls -l "$out.xdelta" "$out.zip"
