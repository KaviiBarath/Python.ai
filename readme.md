# ⚡ STARK
### Advanced Real-Time Voice AI Desktop Assistant
**Developed by Barath**

STARK is a high-performance, real-time voice AI assistant powered by Google Gemini Live API. It features bidirectional voice conversation, visual perception, intelligent system automation, persistent long-term memory, and a lightweight software-rendered holographic interface.

---

## ✨ Key Features

### 🎙️ Real-Time Multimodal Voice & Vision
- **Ultra-Low Latency Voice Streaming**: Direct real-time bidirectional audio conversation via Gemini Live API.
- **Visual Intelligence**: Screen capture and webcam feed processing for live context-aware reasoning.
- **Formant & Viseme Lip-Sync**: High-precision mouth movements synchronized with speech using audio formants and phonetic analysis.
- **Holographic HUD & Avatar**: Software-rendered animated face and reactive waveform HUD with zero GPU overhead.
- **Echo Cancellation & Push-to-Talk**: Built-in self-echo protection and global push-to-talk hotkey support.

### 🖥️ Desktop & System Automation
- **System Control**: Adjust volume, brightness, power state, network settings, and shortcuts by voice.
- **App & Browser Control**: Launch applications, manage windows, browse websites, and automate web workflows.
- **File & Document Processing**: Read, search, organize, and summarize documents (PDF, DOCX, XLSX, TXT).
- **Proactive Insights & Reminders**: Scheduled reminders, automated system health telemetry (CPU/RAM/GPU), and morning briefings.
- **Interactive Dev Assistant**: Integrated code review, terminal task execution, and automated assistant tools.

### 🧠 Intelligent Memory & Safety
- **Persistent Local Memory**: Long-term context storage with fast indexed local search across sessions.
- **Language Adaptation**: Automatically detects and speaks the user's preferred language seamlessly.
- **Action Undo Engine**: Ability to safely roll back recent file operations and settings changes.
- **Confirmation Gate**: UI confirmation dialogs for critical system operations (shutdown, reboot, network changes).
- **Drop-in Plugin Architecture**: Easily extend capabilities by adding Python modules to the `plugins/` directory.

---

## 🏗️ Architecture & Modules

| Directory / File | Description |
|---|---|
| `main.py` | Main application loop, audio stream management, Gemini Live session handling, and dispatch engine |
| `ui.py` | PyQt6 desktop interface, animated holographic HUD, audio waveforms, activity log, and settings drawer |
| `actions/` | Core automation suite (system settings, file management, web search, app launcher, screen analysis, etc.) |
| `core/` | Core subsystems (viseme extraction, prompt management, hotkeys, undo engine, confirmation gate, STT/TTS) |
| `memory/` | Long-term memory store, configuration manager, and persistent session state |
| `plugins/` | Modular plugin framework for drop-in custom skills and integrations |
| `setup.py` | Cross-platform automated environment and dependency installer |

---

## 🚀 Quick Start

### 1. Requirements
- **Python**: 3.11 or newer
- **Microphone & Speaker**: Required for real-time voice streaming
- **Gemini API Key**: Free API key from Google AI Studio
- **OS**: Windows, macOS, or Linux (No external GPU required)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/stark.git
cd stark

# Run automated setup
python setup.py

# Launch STARK
python main.py
```

*Alternative manual installation:*
```bash
pip install -r requirements.txt
python main.py
```

On first launch, enter your Gemini API key in the configuration prompt to initialize the assistant.

---

## 🔒 Privacy & Security

- **Local Execution**: All memories, settings, and credentials remain locally stored on your machine.
- **No Third-Party Tracking**: Audio and vision data stream strictly to your Gemini Live endpoint during active turns.
- **Safe Operations**: Destructive system commands require explicit human confirmation via the interface.

---

## 📄 License

This project is licensed for personal and non-commercial use.
