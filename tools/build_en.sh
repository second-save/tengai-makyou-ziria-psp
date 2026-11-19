#!/bin/bash
# Full English build: rom/ -> build/NPJJ30029/CONTENT.DAT
#   1. unpack CONTENT.DAT's data track (work/ziria_02.iso)
#   2. turn it into the Redump Revision 7 track LIPEMCO's build needs (their base/ code blocks over ours)
#   3. restyle their script to our rulings (tools/restyle.py)
#   4. run their build (vendor/tenmatools, copied to work/tenmatools so vendor/ stays clean)
#   5. repack the translated track into CONTENT.DAT (tools/build.py)
# Needs: python3, g++, make, cmake, libpng and ImageMagick (brew install libpng imagemagick).
set -o errexit -o pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3}
export CPATH=/opt/homebrew/include LIBRARY_PATH=/opt/homebrew/lib

shasum -c rom.sha1
mkdir -p work
$PY tools/content_xor.py rom/NPJJ30029/CONTENT.DAT work/content.plain
$PY tools/vpce.py x work/content.plain work/content
$PY tools/hcd.py unpack work/content/HCD9005_02.bin work/ziria_02.iso

rsync -a vendor/tenmatools/ work/tenmatools/
$PY tools/make_rev7.py work/ziria_02.iso vendor/tenmatools/tenma work/tenmatools/tenma/tenma_02.iso
$PY tools/restyle.py vendor/tenmatools/tenma/script work/tenmatools/tenma/script

if [ ! -f work/tenmatools/tenma/wla-dx/binaries/wla-huc6280 ]; then   # CMake 4 refuses the old minimum version
  (cd work/tenmatools/tenma/wla-dx && cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -G "Unix Makefiles" . && make)
fi
(cd work/tenmatools/tenma && bash ./build.sh) > work/tenma_build.log 2>&1 || { tail -20 work/tenma_build.log; exit 1; }
grep -q "Success!" work/tenma_build.log || { echo "tenmatools build did not finish: see work/tenma_build.log"; exit 1; }

$PY tools/build.py
