#!/bin/bash

# Run build_clean script
./build_clean.sh

# Run build_app script
./build_app.sh

# Delete build_env directory recursively
rm -rf build_env
