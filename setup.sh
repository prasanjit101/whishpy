#!/bin/zsh

# Copy the application to whish directory, overwriting if it exists
mkdir -p ~/scripts/whish
cp -r main.py src ~/scripts/whish/

# Make the main script executable
chmod +x ~/scripts/whish/main.py
