# 🤝 Contributing to Threadlink

Thank you for your interest in contributing to Threadlink! We're building more than just a tool—we're creating an **open protocol for memory** that helps bridge the gap between AI conversations and the artifacts they inspire.

---

## 🌟 Philosophy

Threadlink is designed as an **open protocol**. This means:

- **Simplicity first** - Keep the core simple and extensible
- **Local-first** - Respect user privacy and file systems
- **Protocol-driven** - Design for interoperability with other tools
- **Community-owned** - Everyone's input shapes the future

---

## 🚀 Quick Start for Contributors

### Prerequisites

- **Python 3.8+**
- **Git**
- **Virtual environment** (recommended)

### Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/thrialectics/threadlink.git
cd threadlink

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install development dependencies
pip install -e ".[dev]"

# 4. Install pre-commit hooks (optional but recommended)
pre-commit install

# 5. Run tests to ensure everything works
pytest
```

### Verify Your Setup

```bash
# Should show help text
threadlink --help

# Run the test suite
pytest -v

# Check code formatting
black --check threadlink/
flake8 threadlink/
```

---

## 🎯 Types of Contributions

We welcome many types of contributions:

### 🐛 Bug Reports
Found something broken? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### ✨ Feature Requests
Have an idea? We'd love to hear it! Include:
- The problem you're trying to solve
- Your proposed solution
- Why it fits with Threadlink's philosophy
- Any implementation ideas

### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Documentation improvements
- Test coverage improvements

### 🔌 Protocol Extensions
- New output formats
- Integration with other tools
- Plugin development
- Protocol specification improvements

### 📝 Documentation
- README improvements
- Code documentation
- Usage examples
- Tutorial content

---

## 🛠️ Development Guidelines

### Code Style

We use **Black** for code formatting and **flake8** for linting:

```bash
# Format code
black threadlink/

# Check linting
flake8 threadlink/

# Type checking
mypy threadlink/
```

### Testing

- Write tests for new features
- Maintain or improve test coverage
- Use descriptive test names
- Test edge cases

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=threadlink

# Run specific test file
pytest tests/test_core.py
```

### Commit Messages

Use clear, descriptive commit messages:

```
✨ Add reverse lookup functionality
🐛 Fix path normalization on Windows
📝 Update README with new examples
🔧 Improve error handling in CLI
```

---

## 📋 Pull Request Process

### Before You Start

1. **Check existing issues** - Is someone already working on this?
2. **Open an issue first** - Discuss larger changes before implementing
3. **Keep changes focused** - One feature/fix per PR

### Submitting Your PR

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Test thoroughly**
   ```bash
   pytest
   black --check threadlink/
   flake8 threadlink/
   ```

4. **Write a clear PR description**
   - What does this change do?
   - Why is it needed?
   - How should it be tested?
   - Any breaking changes?

5. **Submit and iterate**
   - We'll review and provide feedback
   - Address any requested changes
   - Once approved, we'll merge!

---

## 🏗️ Project Structure

```
threadlink/
├── threadlink/          # Main package
│   ├── __init__.py
│   ├── cli.py          # CLI interface
│   ├── core.py         # Core functionality
│   ├── utils.py        # Utility functions
│   └── protocol.py     # Protocol definitions
├── tests/              # Test suite
├── docs/               # Documentation
├── examples/           # Usage examples
└── scripts/            # Development scripts
```

---

## 🌍 Community Guidelines

### Be Respectful
- Welcome newcomers
- Be patient with questions
- Provide constructive feedback
- Celebrate contributions

### Focus on the Protocol
- Think about interoperability
- Consider how changes affect other tools
- Keep the core simple and extensible
- Document protocol changes clearly

### Privacy First
- Never collect user data
- Keep everything local-first
- Respect user file systems
- Be transparent about any external connections

---

## 🎉 Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes for significant contributions
- Special mentions for protocol improvements
- Community showcase for creative implementations

---

## 🤔 Questions?

- **General questions**: Open a [Discussion](https://github.com/thrialectics/threadlink/discussions)
- **Bug reports**: Open an [Issue](https://github.com/thrialectics/threadlink/issues)
- **Feature ideas**: Start with a [Discussion](https://github.com/thrialectics/threadlink/discussions)
- **Protocol questions**: Check the [Protocol Spec](https://github.com/thrialectics/threadlink/blob/main/PROTOCOL.md)

---

## 📄 License

By contributing to Threadlink, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping build the future of conversation memory! 🚀** 