# Contributing to AI Study Buddy

Thanks for your interest in contributing! 🎉 This project is an AI-powered tutoring application built with Streamlit and the Google Gemini API. Whether you're fixing a bug, improving documentation, or adding a feature, your help is appreciated.

Please read the [README](README.md) first to understand the project and its architecture, and check the [docs](docs/) folder for detailed technical documentation.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Requesting Features](#requesting-features)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Commit Guidelines](#commit-guidelines)
- [Project Structure](#project-structure)

---

## Code of Conduct

Be respectful and constructive. This project is a learning/capstone project, so reviewers and contributors are often beginners — patience and kindness go a long way. Harassment of any kind is not tolerated.

## Getting Started

1. **Fork the repository** and clone your fork.
2. **Set up the environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Configure your API key:**
   ```bash
   cp .env.example .env
   # then edit .env and add your real values
   ```

   > A Gemini API key is free from [Google AI Studio](https://aistudio.google.com/app/apikey). Many parts of the app (e.g. quiz, feedback) need a key, but parts work offline.

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## How to Contribute

### Reporting Bugs

Before opening an issue, please:

- Search the [open issues](https://github.com/komalharshita/ai-study-buddy/issues) to make sure the bug wasn't already reported.
- Reproduce the bug and note your environment (Python version, OS, Streamlit version).

When filing an issue, include:

- A clear, descriptive title.
- Steps to reproduce.
- What you expected to happen vs. what actually happened.
- Any relevant error messages or logs.

### Requesting Features

Open an issue with the **Feature request** tag describing:

- The problem the feature solves.
- A rough idea of how it could work.
- Whether it aligns with the project's educational goals.

### Submitting Pull Requests

1. **Keep PRs small and focused.** One PR per concern (bug fix, feature, docs, etc.). Small PRs are reviewed and merged much faster.
2. **Branch from `main`** and name your branch descriptively, e.g. `fix/offline-quiz` or `feat/speech-input`.
3. **Write tests** for any new or changed behavior and make sure the full suite passes (see [Testing](#testing)).
4. **Update documentation** if you change user-facing behavior (README or `docs/`).
5. Open the PR against `main`, link any related issue with `Fixes #123`, and describe what you changed and why.

## Development Workflow

This app is structured in layers:

- `app.py` — Streamlit entry point that wires everything together.
- `src/config.py` — environment-based configuration.
- `src/core/` — Gemini client wrapper and persona/prompt templates.
- `src/ui/` — reusable UI components and injected CSS.
- `src/utils/` — JSON extraction and schema validation helpers.
- `tests/` — pytest suite (mock the Gemini SDK; never call the live API).

Keep single-responsibility in mind: UI shouldn't talk to the API directly, and core logic shouldn't know about Streamlit.

## Code Style

- Python 3.10+; follow [PEP 8](https://peps.python.org/pep-0008/) conventions.
- Use descriptive function names and, where helpful, short docstrings.
- **No comments required** — prefer clear, self-documenting code.
- Keep line lengths reasonable and imports organized (stdlib → third-party → local).

## Testing

The project uses `pytest` and `pytest-mock`.

```bash
pytest tests/ -v
```

Guidelines:

- Never make real network calls to the Gemini API in tests.
- Mock the SDK with `unittest.mock` / `pytest-mock` (see `tests/test_gemini_client.py`).
- Add a test for any new logic — if it can break, it should be tested.

The repository runs this suite automatically on every push and pull request via GitHub Actions (`.github/workflows/ci.yml`).

## Commit Guidelines

- Use conventional commit prefixes: `feat:`, `fix:`, `docs:`, `ci:`, `chore:`, `refactor:`, `test:`.
- Write a short summary line, then a body explaining the *why* when it's not obvious.
- Reference issues with `Fixes #123` in the body when the commit closes one.

Examples:

```text
fix: validate sample quiz before loading it into session state

The offline quiz now runs schema validation so malformed data shows a clear error.
Fixes #1
```

## Project Structure

```
ai-study-buddy/
├── app.py                      # Streamlit entry point
├── src/                        # Source code namespace
│   ├── config.py               # Environment configuration
│   ├── logger.py               # Logging setup
│   ├── core/                   # Gemini client + persona/prompts
│   ├── ui/                     # UI components and styles
│   └── utils/                  # Parsing and validation helpers
├── tests/                      # pytest suite
├── data/                       # Offline/sample assets (quiz, transcript, reflection)
├── docs/                       # Technical documentation
├── notebooks/                  # Google Colab notebook
├── scripts/                    # Management utilities
├── Dockerfile                  # Container image
└── docker-compose.yml          # Local container orchestration
```