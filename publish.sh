#!/bin/bash

# Pac-Man Itch.io packing & publishing script
# Authors: abani-am, ialalwn

set -e

BUILD_DIR="packaging/build"
USERNAME="Ahmadalameri-0"
GAME="pacman"

echo "Building the executable for Linux via Makefile..."
make build

echo "Cleaning previous package directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "Copying compiled game to package directory..."
cp -r dist/Pac-Man42/* "$BUILD_DIR"

echo "Adding in-package instructions..."
cat > "$BUILD_DIR/README.txt" << 'EOF'
Pac-Man 42 - Quick Start
==========================
Controls: Arrow keys / WASD to move, ESC to pause.
Run: Just double-click or run ./Pac-Man42 from the terminal.
Config: edit config.json to customize lives, points, levels, etc.
Cheat mode: press [F1-F5] during gameplay.
EOF

echo "Publishing to Itch.io..."
butler push "$BUILD_DIR" "$USERNAME/$GAME:linux"
 
echo "Done! The game is live on Itch.io"