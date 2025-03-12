#!/bin/zsh

# Copy the srcipts to whish.py, overwriting if it exists
mkdir -p ~/scripts
cp main.py ~/scripts/whish.py

# Make the copied script executable
chmod +x ~/scripts/whish.py
