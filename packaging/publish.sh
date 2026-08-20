#!/bin/bash

# Pac-Man Itch.io packing & publishing script
# Authors: abani-am, ialalwn

set -e

BUILD_DIR="packing/build"
USERNAME-"Ahmadalameri-0"
GAME="pacman"

echo "Cleaning previous build.."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "Copying source and assets..."
cp -r entities configuration_files assets libs \
      config.json pyproject.toml pac-man.py \
      "$BUILD_DIR"

echo "Adding in-package instructions..."
cat > "$BUILD_DIR/README.txt" << 'EOF'
Pac-Man 42 - Quick Start
==========================
Controls: Arrow keys / WASD to move, ESC to pause.
Run: python pac-man.py config.json
Config: edit config.json to customize lives, points, levels, etc.
Cheat mode: press [key] during gameplay.
EOF

echo "Publishing to Itch.io..."
butler push "$BUILD_DIR" "$USERNAME/$GAME:linux"
 
echo "Done"