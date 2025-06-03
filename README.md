# 🔗 Threadlink

> **Let your documents remember your conversations.**

Threadlink is a lightweight CLI tool that creates persistent links between AI conversations and your local files. It's a protocol for memory—a way to trace any document back to the conversation that sparked it.

---

## ✨ The Problem

You have a great conversation with ChatGPT. It leads to a document, a design, some code. Two weeks later, you're looking at the file and wondering: 

> *"What was the context? What was I thinking?"*

**Threadlink solves this** by creating a simple, local-first connection between your AI conversations and the artifacts they inspire.

---

## 🚀 Quick Start

### Installation

```bash
# Install from GitHub
pip install git+https://github.com/thrialectics/threadlink.git

# Or clone and install locally
git clone https://github.com/thrialectics/threadlink.git
cd threadlink
pip install -e .
```

### Basic Usage

```bash
# 1. Create a thread reference
threadlink quick "Discussing API design patterns" https://chat.openai.com/c/abc123

# 2. Attach files to the thread
threadlink attach api_design_2025-06-02 ~/Documents/api_spec.md
threadlink attach api_design_2025-06-02 ~/Code/prototype.py

# 3. Later: "What conversation led to this file?"
threadlink reverse ~/Documents/api_spec.md
# → Shows thread summary, chat URL, and linked files

# 4. Search your memory
threadlink search "API design"
```

---

## 🧠 Core Concepts

Threadlink uses a simple JSON index (`~/.threadlink/thread_index.json`) to maintain links between:

| Component | Description |
|-----------|-------------|
| **Thread IDs** | Human-readable tags or UUIDs that identify conversations |
| **Chat URLs** | Direct links back to the source conversation |
| **Local Files** | Any documents, images, or code connected to that thread |
| **Metadata** | Summaries, timestamps, and context |

---

## 📖 Commands Reference

### Create a new thread

```bash
# With custom tag
threadlink new --tag project_x --summary "Project X brainstorming" --chat_url "https://..."

# Auto-generated tag
threadlink quick "Project X brainstorming" "https://..."
```

### Link files to threads

```bash
threadlink attach project_x ~/Documents/project_x_notes.md
```

### Find threads from files

```bash
threadlink reverse ~/Documents/project_x_notes.md
```

### Search your thread history

```bash
threadlink search "project"
```

### View thread details

```bash
threadlink show project_x
```

---

## 🎯 Use Cases

### 📁 Scenario 1: "Where did this file come from?"

You're browsing your projects folder and find some old designs. What were they for?

```bash
threadlink reverse ~/Projects/old_design.png
# → Links back to the ChatGPT conversation that inspired them
```

### 🔍 Scenario 2: "I need to revisit that conversation"

You remember discussing something important but can't find the chat:

```bash
threadlink search "authentication"
# → Finds all threads about authentication with their links
```

### 🚀 Scenario 3: "Keep this project's context together"

You're starting a new project with AI assistance:

```bash
threadlink quick "New startup idea discussion" "https://chat.openai.com/c/..."
threadlink attach new_startup_idea_2025-06-02 ~/Projects/startup/plan.md
threadlink attach new_startup_idea_2025-06-02 ~/Projects/startup/pitch.pdf
```

---

## 🔧 Advanced Features

- **🏷️ Dual-mode tags**: Use human-readable tags or let the system generate UUIDs
- **📂 Path normalization**: Handles `~`, relative paths, and symlinks
- **🔍 Flexible search**: Search by tag name or summary content
- **🔌 Protocol-based**: Designed to be extended by other tools and plugins

---

## 🗺️ Roadmap

- [ ] **🌐 Browser extension** for one-click thread creation
- [ ] **📝 Obsidian/Notion/VSCode plugins**
- [ ] **🧠 Semantic search** across thread content
- [ ] **👥 Team sharing** and sync options
- [ ] **🖥️ GUI** for non-terminal users

---

## 🤝 Contributing

Threadlink is designed as an **open protocol**. We welcome:

- 🐛 Bug reports and feature requests
- 🔌 Plugin development for other tools
- 📋 Protocol extensions and improvements

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details.

---

## 📄 License

**MIT License** - see [`LICENSE`](LICENSE) file.

---

## 🌟 Philosophy

> Threadlink isn't trying to be another PKM tool or AI wrapper. It's a **protocol for memory**—a way to maintain context across the gap between conversation and creation. 

It respects your file system, your privacy, and your existing workflows.

---

<div align="center">

**Built with ❤️ by [Marianne](https://github.com/thrialectics)**

[Thread Protocol Spec](https://github.com/thrialectics/threadlink/blob/main/PROTOCOL.md) | [Documentation](https://github.com/thrialectics/threadlink#readme) | [Examples](https://github.com/thrialectics/threadlink/tree/main/examples)

</div>