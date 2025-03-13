"""
Setup configuration for building whishpy.app using py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = ['whishpy.png']
OPTIONS = {
    'argv_emulation': False,
    'packages': ['rumps', 'src'],
    'iconfile': 'whishpy.png',
    'plist': {
        'CFBundleName': 'Whishpy',
        'CFBundleDisplayName': 'Whishpy',
        'CFBundleIdentifier': 'com.whishpy.app',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'LSMinimumSystemVersion': '10.10',
        'NSMicrophoneUsageDescription': 'This app needs access to the microphone to record audio for transcription.',
        'NSPasteboardUsageDescription': 'This app needs access to the clipboard to paste transcribed text.',
        'NSHighResolutionCapable': True,
    },
    'resources': ['whishpy.png'],
    'excludes': ['tkinter', 'matplotlib', 'numpy', 'pandas'],
}

setup(
    name='Whishpy',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'rumps>=0.4.0',
        'pyobjc-framework-Cocoa',
    ],
)
