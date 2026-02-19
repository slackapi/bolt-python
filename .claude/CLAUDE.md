# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Slack Bolt for Python -- a framework for building Slack apps. Built on top of `slack_sdk>=3.38.0,<4`. Supports both sync (`App`) and async (`AsyncApp`) patterns, with adapters for Flask, FastAPI, Django, AWS Lambda, and many other frameworks.

## Environment Setup

A virtual environment (`.venv`) should be activated before running any commands. If tools like `black`, `flake8`, or `pytest` are not found, ask the user to activate the venv.

## Common Commands

### Testing
```bash
# Run all tests (installs deps, formats, lints, tests, typechecks)
./scripts/install_all_and_run_tests.sh

# Run a single test file
./scripts/run_tests.sh tests/scenario_tests/test_app.py

# Run a single test directly (skip formatting)
pytest -vv tests/scenario_tests/test_app.py

# Run a single test function
pytest -vv tests/scenario_tests/test_app.py::TestApp::test_name
```

### Formatting, Linting, Type Checking
```bash
# Format (black, line-length=125)
./scripts/format.sh --no-install

# Lint (flake8, line-length=125, ignores: F841,F821,W503,E402)
./scripts/lint.sh --no-install

# Type check (mypy)
./scripts/run_mypy.sh --no-install
```

### First-Time Setup
```bash
pip install -U -e .
pip install -U -r requirements/testing.txt
pip install -U -r requirements/adapter.txt
pip install -U -r requirements/adapter_testing.txt
pip install -U -r requirements/tools.txt
```

## Architecture

### Request Processing Pipeline

Incoming requests flow through a middleware chain before reaching listeners:

1. **SSL Check** -> **Request Verification** (signature) -> **URL Verification** -> **Authorization** (token injection) -> **Ignoring Self Events** -> Custom middleware
2. **Listener Matching** -- `ListenerMatcher` implementations check if a listener should handle the request
3. **Listener Execution** -- listener-specific middleware runs, then `ack()` is called, then the handler executes

For FaaS environments (`process_before_response=True`), long-running handlers execute as "lazy listeners" in a thread pool after the ack response is returned.

### Core Abstractions

- **`App` / `AsyncApp`** (`slack_bolt/app/`) -- Central class. Registers listeners via decorators (`@app.event()`, `@app.action()`, `@app.command()`, `@app.message()`, `@app.view()`, `@app.shortcut()`, `@app.options()`, `@app.function()`). Dispatches incoming requests through middleware to matching listeners.
- **`Middleware`** (`slack_bolt/middleware/`) -- Abstract base with `process(req, resp, next)`. Built-in: authorization, request verification, SSL check, URL verification, assistant, self-event ignoring.
- **`Listener`** (`slack_bolt/listener/`) -- Has matchers, middleware, and an ack/handler function. `CustomListener` is the main implementation.
- **`ListenerMatcher`** (`slack_bolt/listener_matcher/`) -- Determines if a listener handles a given request. Built-in matchers for events, actions, commands, messages (regex), shortcuts, views, options.
- **`BoltContext`** (`slack_bolt/context/`) -- Dict-like object passed to listeners with `client`, `say()`, `ack()`, `respond()`, `complete()`, `fail()`, plus event metadata (`user_id`, `channel_id`, `team_id`).
- **`BoltRequest` / `BoltResponse`** (`slack_bolt/request/`, `slack_bolt/response/`) -- Request/response wrappers. Request has `mode` of "http" or "socket_mode".

### Kwargs Injection

Listeners receive arguments by parameter name. The framework inspects function signatures and injects matching args: `body`, `event`, `action`, `command`, `payload`, `context`, `client`, `ack`, `say`, `respond`, `logger`, `complete`, `fail`, `agent`, etc. Defined in `slack_bolt/kwargs_injection/args.py`.

### Adapter System

Each adapter in `slack_bolt/adapter/` converts between a web framework's request/response types and `BoltRequest`/`BoltResponse`. Adapters exist for: Flask, FastAPI, Django, Starlette, Sanic, Bottle, Tornado, CherryPy, Falcon, Pyramid, AWS Lambda, Google Cloud Functions, Socket Mode, WSGI, ASGI, and more.

### Async Support

`AsyncApp` mirrors `App` with async middleware, listeners, and context utilities. Located in `slack_bolt/app/async_app.py`. Requires `aiohttp`. All async variants live alongside their sync counterparts (e.g., `async_middleware.py` next to `middleware.py`).

### AI Agents & Assistants

`BoltAgent` (`slack_bolt/agent/`) provides `chat_stream()`, `set_status()`, and `set_suggested_prompts()` for AI-powered agents. `Assistant` middleware (`slack_bolt/middleware/assistant/`) handles assistant thread events.

## Test Organization

- `tests/scenario_tests/` -- Integration-style tests with realistic Slack payloads
- `tests/slack_bolt/` -- Unit tests mirroring the source structure
- `tests/adapter_tests/` and `tests/adapter_tests_async/` -- Framework adapter tests
- `tests/mock_web_api_server/` -- Mock Slack API server used by tests
- Async test variants use `_async` suffix directories

## Code Style

- **Black** formatter, 125 char line length
- **Flake8** linter, 125 char line length
- **MyPy** with `force_union_syntax=true` and `warn_unused_ignores=true` (use `X | Y` union syntax, not `Union[X, Y]`)
- pytest with `asyncio_mode = "auto"`
