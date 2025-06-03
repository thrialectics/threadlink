# 🔗 Threadlink Protocol Specification

**Version:** 1.0  
**Status:** Draft  
**Updated:** 2025-06-03

---

## Abstract

Threadlink is a lightweight, durable linkage between ephemeral conversation threads and persistent artifacts. This specification defines a minimal, local-first protocol for creating and maintaining these linkages across different tools and platforms.

---

## 1. Core Concepts

### 1.1 What is a Thread?

A **thread** represents an ephemeral conversation or interaction session, typically with an AI assistant, that has:

- **Temporal existence**: A conversation that occurred at a specific time
- **Contextual boundary**: A coherent discussion about specific topics
- **External reference**: Usually accessible via URL or identifier
- **Knowledge artifacts**: Generated or referenced documents, code, designs, etc.

**Examples:**
- A ChatGPT conversation about API design
- A Claude session about code review
- A brainstorming discussion that led to documentation
- A problem-solving conversation that produced solutions

### 1.2 What is a Link?

A **link** is a bidirectional association between:

1. **Thread metadata** (conversation context, URL, summary)
2. **Local artifacts** (files, documents, code, designs)

Links enable:
- **Forward tracing**: "What files came from this conversation?"
- **Reverse tracing**: "What conversation created this file?"
- **Context preservation**: Maintaining the reasoning behind artifacts

### 1.3 What is a Binding?

A **binding** is the concrete representation of a link, consisting of:

- **Thread identifier** (human-readable or UUID)
- **Thread metadata** (summary, URL, timestamps)
- **Artifact references** (file paths, URIs)
- **Relationship semantics** (created, referenced, inspired, etc.)

---

## 2. Minimal Schema

### 2.1 Thread Index Structure

The core data structure is a JSON object stored in `~/.threadlink/thread_index.json`:

```json
{
  "thread_id": {
    "summary": "string",
    "linked_files": ["string"],
    "chat_url": "string",
    "date_created": "ISO8601",
    "auto_generated": "boolean",
    "protocol_version": "string",
    "metadata": {
      "platform": "string",
      "tags": ["string"],
      "relationship": "string"
    }
  }
}
```

### 2.2 Required Fields

**Minimal binding schema:**

```json
{
  "thread_id": {
    "summary": "Brief description of the conversation",
    "linked_files": ["/path/to/artifact1", "/path/to/artifact2"],
    "date_created": "2025-06-03T10:30:00.000Z"
  }
}
```

### 2.3 Optional Fields

**Extended binding schema:**

```json
{
  "thread_id": {
    "summary": "Brief description of the conversation",
    "linked_files": ["/path/to/artifact1"],
    "chat_url": "https://platform.com/conversation/id",
    "date_created": "2025-06-03T10:30:00.000Z",
    "date_modified": "2025-06-03T15:45:00.000Z",
    "auto_generated": true,
    "protocol_version": "1.0",
    "metadata": {
      "platform": "chatgpt",
      "tags": ["api-design", "architecture"],
      "relationship": "created",
      "confidence": 0.9,
      "user_notes": "Initial brainstorming session"
    }
  }
}
```

### 2.4 Thread ID Conventions

**Human-readable format** (recommended):
- Pattern: `{topic}_{date}_{optional_suffix}`
- Example: `api_design_2025-06-03`
- Characters: `[a-z0-9_-]` only
- Length: 100 characters maximum

**UUID format** (fallback):
- Standard UUID4 format
- Example: `f47ac10b-58cc-4372-a567-0e02b2c3d479`
- Used when auto-generating or avoiding conflicts

---

## 3. File System Conventions

### 3.1 Storage Location

**Primary index:**
- Path: `~/.threadlink/thread_index.json`
- Permissions: `600` (owner read/write only)
- Encoding: UTF-8
- Format: JSON with 2-space indentation

**Directory structure:**
```
~/.threadlink/
├── thread_index.json          # Primary index
├── backups/                   # Automatic backups
│   ├── thread_index.2025-06-03.json
│   └── thread_index.2025-06-02.json
├── exports/                   # Protocol exports
└── plugins/                   # Extension data
```

### 3.2 File Path Conventions

**Absolute paths** (preferred):
- Use resolved, canonical paths
- Example: `/Users/alice/Documents/project_notes.md`

**Relative paths** (for portability):
- Relative to user home: `~/Documents/project_notes.md`
- Relative to current working directory: `./notes.md`

**Path normalization rules:**
1. Expand `~` to user home directory
2. Resolve `.` and `..` components
3. Follow symlinks to canonical paths
4. Use forward slashes on all platforms

---

## 4. Implementation Guidelines

### 4.1 How Systems Should Expose Bindings

**API Surface:**

```python
# Core operations
create_thread(id, summary, chat_url=None, metadata=None)
link_artifact(thread_id, file_path, relationship="created")
find_thread_by_artifact(file_path)
find_artifacts_by_thread(thread_id)
search_threads(query, filters=None)

# Metadata operations  
get_thread_metadata(thread_id)
update_thread_metadata(thread_id, metadata)
get_thread_stats()
```

**Command Line Interface:**

```bash
# Thread management
threadlink new --tag <id> --summary "<text>" --url "<url>"
threadlink show <thread_id>
threadlink search "<query>"

# Artifact linking
threadlink attach <thread_id> <file_path>
threadlink detach <thread_id> <file_path>
threadlink reverse <file_path>

# Export/import
threadlink export --format json|csv|yaml
threadlink import --file <path> --format json|csv|yaml
```

### 4.2 How Systems Should Consume Bindings

**Read-only consumption:**

```python
import json
from pathlib import Path

def load_thread_index():
    index_path = Path.home() / ".threadlink" / "thread_index.json"
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def get_thread_for_file(file_path):
    index = load_thread_index()
    resolved_path = str(Path(file_path).resolve())
    
    for thread_id, data in index.items():
        if resolved_path in data.get('linked_files', []):
            return thread_id, data
    return None, None
```

**Integration patterns:**

1. **Editor plugins**: Show thread context in file headers
2. **Browser extensions**: Auto-create threads from chat URLs
3. **Project tools**: Include thread references in project metadata
4. **Documentation generators**: Link conversations to generated docs

### 4.3 Atomic Operations

**Safe write pattern:**

```python
def update_thread_index(updates):
    index_path = Path.home() / ".threadlink" / "thread_index.json"
    temp_path = index_path.with_suffix('.tmp')
    
    # Load current data
    current_data = load_thread_index()
    
    # Apply updates
    current_data.update(updates)
    
    # Atomic write
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)
    
    temp_path.replace(index_path)
    index_path.chmod(0o600)
```

---

## 5. Protocol Guarantees

### 5.1 Durability

**Strong guarantees:**
- **Data persistence**: Thread index survives system restarts
- **Atomic updates**: No partial writes or corrupted states
- **Backup creation**: Automatic backups on corruption detection
-  **Error recovery**: Graceful handling of malformed data

**Weak guarantees:**
- **Cross-device sync**: No automatic synchronization
- **Concurrent access**: Basic file locking, no distributed coordination
- **Version migration**: Best-effort compatibility across protocol versions

### 5.2 Locality

**Guarantees:**
- **Local-first**: All data stored locally by default
- **No external dependencies**: Protocol works offline
- **Privacy-preserving**: No automatic data transmission
- **User control**: Complete ownership of data and access patterns

**Implications:**
- Chat URLs are stored but never automatically accessed
- File paths reference local artifacts only
- No cloud storage or external API requirements
- Suitable for sensitive or proprietary information

### 5.3 Mutability

**Thread metadata:**
- **Mutable**: Summary, tags, metadata can be updated
- **Append-only**: File lists typically grow over time
- **Timestamp preservation**: `date_created` immutable, `date_modified` updated

**File associations:**
- **Dynamic**: Files can be linked/unlinked from threads
- **Many-to-many**: Files can belong to multiple threads
- **Path updates**: File paths updated when files move

**Thread identity:**
- **Stable**: Thread IDs should not change once created
- **Collision handling**: Duplicate IDs handled gracefully
- **Deletion support**: Threads can be removed entirely

---

## 6. Versioning & Compatibility

### 6.1 Protocol Versioning

**Semantic versioning**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes to core schema or guarantees
- **MINOR**: Backward-compatible additions (new fields, operations)
- **PATCH**: Bug fixes, clarifications, non-functional improvements

**Current version**: `1.0`

### 6.2 Backward Compatibility

**Schema evolution rules:**

1. **New optional fields**: Always allowed in minor versions
2. **Required fields**: Never removed, only deprecated
3. **Field semantics**: Meaning cannot change within major version
4. **Default values**: Must be provided for new fields

**Migration strategy:**

```json
{
  "protocol_version": "1.0",
  "deprecated_fields": {
    "old_field": "Use new_field instead"
  },
  "version_migrations": {
    "0.9": "Auto-migrate on first access"
  }
}
```

### 6.3 Implementation Compatibility

**Reference implementation**: This CLI tool serves as the canonical implementation for testing compatibility.

**Compliance levels:**

1. **Core**: Supports minimal schema + basic operations
2. **Standard**: Supports extended schema + metadata
3. **Extended**: Supports plugins + advanced features

---

## 7. Security Considerations

### 7.1 Data Protection

**File permissions:**
- Thread index: `600` (owner only)
- Backup files: `600` (owner only)
- Plugin data: `700` directory, `600` files

**Input validation:**
- All user inputs sanitized
- File paths validated against traversal attacks
- URL schemes restricted to `http`/`https`
- String length limits enforced

### 7.2 Privacy

**Information exposure:**
- Chat URLs may contain conversation content
- File paths reveal directory structure
- Timestamps indicate activity patterns

**Mitigation strategies:**
- User education about URL sharing
- Option to use relative paths
- Configurable data retention policies

---

## 8. Extension Points

### 8.1 Plugin Architecture

**Plugin directory**: `~/.threadlink/plugins/`

**Plugin manifest** (`plugin.json`):

```json
{
  "name": "browser-extension",
  "version": "1.0.0",
  "protocol_version": "1.0",
  "hooks": {
    "thread_created": "on_thread_created.js",
    "file_linked": "on_file_linked.py"
  },
  "permissions": ["read_index", "write_metadata"]
}
```

### 8.2 Integration Hooks

**Browser extensions:**
- Auto-detect conversation URLs
- Create threads from chat interfaces
- Show file context in web interfaces

**Editor plugins:**
- Display thread context in file headers
- Quick navigation to related conversations
- Auto-link newly created files

**Project tools:**
- Include thread references in `package.json`, `Cargo.toml`
- Generate documentation with conversation links
- CI/CD integration for artifact tracking

---

## 9. Examples

### 9.1 Basic Workflow

```bash
# 1. Create thread from conversation
threadlink quick "API design discussion" "https://chat.openai.com/c/abc123"

# 2. Link artifacts as they're created
threadlink attach api_design_2025-06-03 ./api_spec.md
threadlink attach api_design_2025-06-03 ./routes.py
threadlink attach api_design_2025-06-03 ./tests.py

# 3. Later: find conversation from file
threadlink reverse ./api_spec.md
```

### 9.2 Integration Example

**VSCode extension pseudocode:**

```typescript
// Show thread context in file header
function showThreadContext(filePath: string) {
  const thread = threadlink.findThreadByFile(filePath);
  if (thread) {
    vscode.window.showInformationMessage(
      `💭 From conversation: ${thread.summary}`
    );
  }
}

// Auto-link new files to active thread
function onFileCreated(filePath: string) {
  const activeThread = getActiveThread();
  if (activeThread) {
    threadlink.linkFile(activeThread.id, filePath);
  }
}
```

---

## 10. Future Considerations

### 10.1 Planned Extensions

- **Semantic search**: Vector embeddings for content-based search
- **Collaboration**: Multi-user sharing with permission models
- **Synchronization**: Optional cloud sync with end-to-end encryption
- **Rich metadata**: Support for images, audio, video references

### 10.2 Research Areas

- **Automatic linking**: AI-powered detection of conversation-artifact relationships
- **Context preservation**: Embedding conversation context directly in files
- **Workflow integration**: Deep integration with development and creative tools
- **Federated networks**: Peer-to-peer sharing of thread networks

---

## License

This protocol specification is released under the MIT License, encouraging broad adoption and implementation across tools and platforms.

---

## References

- [JSON Schema Specification](https://json-schema.org/)
- [RFC 3339 - Date and Time on the Internet](https://tools.ietf.org/html/rfc3339)
- [Semantic Versioning](https://semver.org/)
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) 