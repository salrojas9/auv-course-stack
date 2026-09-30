#!/usr/bin/env bash
# check_hunt.sh — grades the Week 0.3 treasure hunt
HUNT="$HOME/hunt"
pass=0; total=4
ok(){ echo "[OK ] $1"; pass=$((pass+1)); }
no(){ echo "[FAIL] $1"; }

[ -d "$HUNT/answer" ] \
  && ok "answer/ folder exists" \
  || no "answer/ folder missing (mkdir ~/hunt/answer)"

[ -f "$HUNT/answer/found.txt" ] \
  && ok "answer/found.txt exists" \
  || no "found.txt missing (touch ~/hunt/answer/found.txt)"

grep -q "HEADING 095" "$HUNT/answer/secret_heading.txt" 2>/dev/null \
  && ok "secret file copied into answer/ (contents intact)" \
  || no "secret_heading.txt not in answer/, or contents changed (use cp)"

[ ! -e "$HUNT/wreck/bridge/secret_heading.txt" ] \
  && ok "original secret removed from the wreck" \
  || no "original still at wreck/bridge/ (use rm — after copying!)"

echo
if [ "$pass" -eq "$total" ]; then
  echo "TREASURE HUNT COMPLETE ($pass/$total). Lesson 0.3 checkpoint earned."
else
  echo "$pass/$total — fix the FAIL lines and rerun: bash check_hunt.sh"
fi
