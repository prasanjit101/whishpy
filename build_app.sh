#!/bin/bash

# Exit on error
set -e

echo "🧹 Cleaning up previous builds..."
rm -rf build dist *.pyc __pycache__ *.egg-info

# Ensure we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Not in a virtual environment. Please activate your virtual environment first."
    exit 1
fi

echo "📦 Installing required packages..."
pip install -r requirements.txt
pip install py2app

echo "🏗️ Building application..."
python setup.py py2app -A

if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully!"
    echo "📱 The app is available in the ./dist directory"
    echo "🚀 To run the app, open: ./dist/Whishpy.app"
else
    echo "❌ Build failed!"
    exit 1
fi 