# Whishpy - Voice-to-Text Transcription for macOS

## Agent Overview

The Whishpy system consists of multiple interconnected agents/components that work together to provide a seamless voice-to-text transcription experience on macOS. This document outlines the architecture, functionality, and operation of these agents.

## System Purpose

Whishpy is designed to provide a seamless voice-to-text solution for macOS users, addressing the inconvenience of manual typing for text input and the need for quick voice note transcription. The system aims to deliver intuitive and easy-to-use functionality with minimal latency and reliable, stable performance.

## Core Components (Agents)

### 1. Menu Bar Interface Agent
- **Role**: Primary user interface using rumps framework
- **Responsibilities**:
  - Display microphone icon in menu bar
  - Handle user interactions (click-to-start/stop recording)
  - Provide settings menu for API key configuration
  - Enable auto-start on login functionality

### 2. Audio Recorder Agent
- **Technology**: Built using PyAudio
- **Functionality**:
  - Handles audio capture from microphone
  - Manages recording start/stop operations
  - Implements max recording time feature with settings management
  - Ensures proper cleanup of audio resources
  - Supports background processing for uninterrupted recording

### 3. Transcription Service Agent
- **Technology**: Groq Whisper API integration
- **Responsibilities**:
  - Manages communication with Groq API for transcription
  - Supports both Groq and OpenAI providers
  - Implements API error handling and retries
  - Caches LLM instances for better performance
  - Handles resource management for API calls
  - Includes fallback mechanisms for better reliability

### 4. LLM Response Generator Agent
- **Technology**: LLM integration (OpenAI/Groq)
- **Functionality**:
  - Generates responses based on transcribed text
  - Provides context-aware responses
  - Handles prompt functionality for user-generated content
  - Implements enhanced error handling for None context parameters
  - Supports language options (English with plans for Hindi, Spanish, French, Japanese)

### 5. Text Inserter Agent
- **Technology**: Uses pynput library
- **Role**: Handles text insertion at cursor position
- **Features**:
  - Direct text insertion instead of clipboard usage
  - Implements Command+V shortcut for text insertion
  - Provides fallback to direct typing if paste shortcut fails
  - Includes fallback to clipboard if text insertion fails
  - Requires accessibility permissions for direct insertion

### 6. Settings Manager Agent
- **Responsibilities**:
  - Centralized configuration management
  - API key management from config file (~/.whishpy/config.json)
  - Provider selection (OpenAI or Groq)
  - User preference storage and retrieval
  - Enhanced security through config file loading

### 7. Circular Logger Agent
- **Functionality**:
  - Provides logging functionality for error tracking
  - Maintains application monitoring capabilities
  - Offers circular logging for efficient storage
  - Supports debugging and issue resolution

## System Architecture

### Design Patterns
- **Event-driven**: Menu actions trigger system responses
- **Asynchronous Processing**: API calls handled without blocking
- **Single Responsibility Principle**: Each component handles specific concerns
- **Modular Design**: Components can be updated independently

### Component Relationship Flow
1. User interacts with Menu Bar Interface Agent
2. Triggers Audio Recorder Agent to start/stop recording
3. Audio Recorder Agent sends data to Transcription Service Agent
4. Transcription Service Agent processes audio and returns text
5. (Optional) Text sent to LLM Response Generator Agent for enhanced responses
6. Text Inserter Agent inserts content at cursor position

### Provider Selection Flow
1. User selects "Set API Key" from menu
2. Application shows API key input and provider selection
3. User enters API key and selects provider (OpenAI or Groq)
4. Configuration saved to ~/.whishpy/config.json
5. TranscriptionService loads provider and API key on initialization
6. LLM instance created with selected provider and API key

## Technical Stack

### Core Technologies
- Python 3.x
- PyAudio for audio capture
- Groq Python library (Whisper for transcription)
- rumps for menu bar interface
- pynput for text insertion
- OpenAI library for LLM integration

### Environment Requirements
- macOS M1 or later
- Virtual environment for dependencies
- API key (Groq or OpenAI)
- Audio permissions
- Accessibility permissions for text insertion

### Dependencies
- rumps, pyaudio, groq, pynput, openai
- Additional LLM libraries as needed

## Security & Permissions

### Required Permissions
- Microphone access for audio recording
- Accessibility access for text insertion at cursor
- File system access for configuration storage

### Security Measures
- API keys stored in secure config file (~/.whishpy/config.json)
- Configuration management through SettingsManager
- Enhanced error handling to prevent data exposure