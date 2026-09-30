#!/usr/bin/env bash
# setup_hunt.sh — builds the Week 0.3 treasure-hunt maze under ~/hunt
set -e
HUNT="$HOME/hunt"
rm -rf "$HUNT"
mkdir -p "$HUNT"/reef/coral "$HUNT"/reef/kelp \
         "$HUNT"/wreck/cargo "$HUNT"/wreck/bridge \
         "$HUNT"/trench/deep

# decoys
echo "just bubbles."                          > "$HUNT/reef/bubbles.txt"
echo "an old map, water-damaged, unreadable." > "$HUNT/wreck/cargo/old_map.txt"
echo "it is very dark down here."             > "$HUNT/trench/deep/darkness.txt"
echo "kelp. so much kelp."                    > "$HUNT/reef/kelp/kelp.txt"

# the treasure
cat > "$HUNT/wreck/bridge/secret_heading.txt" << 'MSG'
HEADING 095
The gate lies at compass heading 095 degrees.
You found this with nothing but cd, ls, and cat. Well navigated.
MSG

echo "Treasure hunt is ready under: $HUNT"
echo "Your mission is in Lesson 0.3, section 5. Begin with:  cd ~/hunt && ls"
