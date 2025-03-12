#!/bin/bash
set -e

echo "Creating a clean build environment..."

# Remove previous build artifacts
rm -rf build dist __pycache__ src/__pycache__

# Create a fresh build directory
mkdir -p build_env

# Create a virtual environment specifically for building
python -m venv build_env/venv
source build_env/venv/bin/activate

# Install only the necessary dependencies
pip install py2app rumps pyaudio groq

# Copy the source files to the build environment
mkdir -p build_env/src
cp -r src/* build_env/src/
cp main.py build_env/
cp whishpy.jpg build_env/
cp setup.py build_env/

# Change to the build directory and build the app
cd build_env
python setup.py py2app

# Copy the built app back to the main dist directory
cd ..
mkdir -p dist
cp -r build_env/dist/* dist/

echo "Build completed. App should be available in dist/Whishpy.app" 