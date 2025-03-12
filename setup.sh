#!/bin/zsh

# Copy main.py to ~/scripts/whish.py, overwriting if it exists
mkdir -p ~/scripts
cp main.py ~/scripts/whish.py

# Make the copied script executable
chmod +x ~/scripts/whish.py
