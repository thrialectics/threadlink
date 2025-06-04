# Threadlink

> **Connect your files with their origin stories**

Threadlink is a lightweight protocol and CLI for creating durable, inspectable links between ephemeral context and persistent files.
Originally designed to track AI conversations and the artifacts they generate, Threadlink also works across tools and systems—wherever you want to trace how an idea became a file, or how a file shaped downstream thinking.

It’s not just a chatbot memory layer. It’s a protocol for context memory—structured, local-first, and composable.

---

## The Problem

You have a great conversation with ChatGPT. It leads to a document, a design, some code. Two weeks later, you're looking at the file and wondering: 

> *"What was the context? What was I thinking?"*

**Threadlink solves this** by creating a simple, local-first connection between your AI conversations and the artifacts they inspire.

---

## Quick Start

### Installation

#### macOS / Linux
```bash
# Install from GitHub
pip install git+https://github.com/thrialectics/threadlink.git

# Or clone and install locally
git clone https://github.com/thrialectics/threadlink.git
cd threadlink
pip install -e .
```

#### Windows
```cmd
# Install from GitHub (Command Prompt)
pip install git+https://github.com/thrialectics/threadlink.git

# Or clone and install locally
git clone https://github.com/thrialectics/threadlink.git
cd threadlink
pip install -e .
```

#### Windows (PowerShell)
```powershell
# Install from GitHub
pip install git+https://github.com/thrialectics/threadlink.git

# Or clone and install locally
git clone https://github.com/thrialectics/threadlink.git
Set-Location threadlink
pip install -e .
```

**Requirements:** Python 3.8+ and Git must be installed on your system.

### Basic Usage

Option A: Name your own thread tag (manual)
```bash
# 1. Create a thread and name it (tag = api_patterns_2025-06-02)
threadlink new --tag api_patterns_2025-06-02 \
               --summary "Discussion of API design patterns" \
               --chat_url https://chat.openai.com/c/abc123
```
```bash
# 2. Attach files to your named thread
threadlink attach api_patterns_2025-06-02 ~/Documents/api_spec.md
threadlink attach api_patterns_2025-06-02 ~/Code/prototype.py
```

Option B: Let Threadlink generate the tag (auto)
```bash
# 1. Create a thread without naming it
threadlink quick "Discussion of API design patterns" https://chat.openai.com/c/abc123
```
```bash
# 2. Copy the tag shown in the output and use it to attach files
threadlink attach threadlink_api_design_2025-06-02 ~/Documents/api_spec.md
```

Later: recall that context
```bash
# “What chat produced this file?”
threadlink reverse ~/Documents/api_spec.md

# “What threads mentioned API design?”
threadlink search "API design"
```
---

## Core Concepts

Threadlink uses a simple JSON index (`~/.threadlink/thread_index.json`) to maintain links between:

| Component | Description |
|-----------|-------------|
| **Thread IDs** | Human-readable tags or UUIDs that identify conversations |
| **Chat URLs** | Direct links back to the source conversation |
| **Local Files** | Any documents, images, or code connected to that thread |
| **Metadata** | Summaries, timestamps, and context |

---

## Commands Reference

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

## Use Cases

### Scenario 1: "Where did this file come from?"

You're browsing your projects folder and find some old designs. What were they for?

```bash
threadlink reverse ~/Projects/old_design.png
# → Links back to the ChatGPT conversation that inspired them
```

### Scenario 2: "I need to revisit that conversation"

You remember discussing something important but can't find the chat:

```bash
threadlink search "authentication"
# → Finds all threads about authentication with their links
```

### Scenario 3: "Keep this project's context together"

You're starting a new project with AI assistance:

```bash
threadlink quick "New startup idea discussion" "https://chat.openai.com/c/..."
threadlink attach new_startup_idea_2025-06-02 ~/Projects/startup/plan.md
threadlink attach new_startup_idea_2025-06-02 ~/Projects/startup/pitch.pdf
```

---

## Advanced Features

- **Dual-mode tags**: Use human-readable tags or let the system generate UUIDs
- **Path normalization**: Handles `~`, relative paths, and symlinks
- **Flexible search**: Search by tag name or summary content
- **Protocol-based**: Designed to be extended by other tools and plugins

---

## The Future of Context Memory

Threadlink is designed to evolve from a personal memory tool into the infrastructure for preserving and sharing human knowledge and reasoning.

### Near-term (6-12 months)
- **One-click capture**: Browser extensions for instant thread creation from any chat
- **Smart linking**: Automated detection of conversation-artifact relationships
- **Visual interfaces**: GUI applications for non-technical users
- **Popular integrations**: Obsidian, Notion, VSCode, and other productivity tools

### Medium-term (1-2 years)
- **Semantic search**: Find conversations by concept and meaning, not just keywords
- **Team collaboration**: Shared thread networks for organizations with privacy controls
- **Knowledge graphs**: Visualize relationships between ideas, conversations, and artifacts
- **Workflow integration**: Deep embedding in creative and analytical processes

### Long-term Vision (2-5 years)
- **Federated networks**: Global knowledge sharing while preserving individual privacy
- **Institutional memory**: Organizations that never lose context, reasoning, or decision history
- **Cross-platform ecosystem**: Universal context preservation across all digital tools
- **New collaboration patterns**: Entirely new ways of building on shared knowledge and reasoning

**This protocol is designed to preserve human context and reasoning across the evolving landscape of digital collaboration.**

---

## Contributing

Threadlink is designed as an **open protocol**. We welcome:

-  Bug reports and feature requests
-  Plugin development for other tools
-  Protocol extensions and improvements

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details.

---

## License

**MIT License** - see [`LICENSE`](LICENSE) file.

---

## Philosophy

> Threadlink isn't trying to be another PKM tool or AI wrapper. It's a **protocol for context memory**—a way to maintain context across the gap between ephemeral conversation and persistent artifact creation. 

It respects your file system, your privacy, and your existing workflows.

---

<div align="center">

**Built by [Marianne](https://github.com/thrialectics)**

[Thread Protocol Spec](https://github.com/thrialectics/threadlink/blob/main/PROTOCOL.md) | [Documentation](https://github.com/thrialectics/threadlink#readme) | [Examples](https://github.com/thrialectics/threadlink/tree/main/examples)

</div>
