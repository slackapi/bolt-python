# AGENTS.md - bolt-python

## Project Overview

Slack Bolt for Python -- a framework for building Slack apps in Python.

- **Foundation:** Built on top of `slack_sdk` (see `pyproject.toml` constraints).
- **Execution Models:** Supports both synchronous (`App`) and asynchronous (`AsyncApp` using `asyncio`) execution. Async mode requires `aiohttp` as an additional dependency.
- **Framework Adapters:** Features built-in adapters for web frameworks (Flask, FastAPI, Django, Tornado, Pyramid, and many more) and serverless environments (AWS Lambda, Google Cloud Functions).
- **Python Version:** Requires Python 3.7+ as defined in `pyproject.toml`.

- **Repository**: <https://github.com/slackapi/bolt-python>
- **Documentation**: <https://docs.slack.dev/tools/bolt-python/>
- **PyPI**: <https://pypi.org/project/slack-bolt/>
- **Current version**: defined in `slack_bolt/version.py` (referenced by `pyproject.toml` via `[tool.setuptools.dynamic]`)

## Environment Setup

A python virtual environment (`venv`) should be activated before running any commands.

```bash
# Create a venv (first time only)
python -m venv .venv

# Activate
source .venv/bin/activate

# Install all dependencies
./scripts/install.sh
```

You can verify the venv is active by checking `echo $VIRTUAL_ENV`. If tools like `black`, `flake8`, `mypy` or `pytest` are not found, ask the user to activate the venv.

## Common Commands

### Testing

Always use the project scripts instead of calling `pytest` directly:

```bash
# Install all dependencies and run all tests (formats, lints, tests, typechecks)
./scripts/install_all_and_run_tests.sh

# Run a single test file
./scripts/run_tests.sh tests/scenario_tests/test_app.py

# Run a single test function
./scripts/run_tests.sh tests/scenario_tests/test_app.py::TestApp::test_name
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
- **`ListenerMatcher`** (`slack_bolt/listener_matcher/`) -- Determines if a listener handles a given request. Built-in matchers for events, actions, commands, messages (regex), shortcuts, views, options, functions.
- **`BoltContext`** (`slack_bolt/context/`) -- Dict-like object passed to listeners with `client`, `say()`, `ack()`, `respond()`, `complete()`, `fail()`, plus event metadata (`user_id`, `channel_id`, `team_id`, etc.).
- **`BoltRequest` / `BoltResponse`** (`slack_bolt/request/`, `slack_bolt/response/`) -- Request/response wrappers. Request has `mode` of "http" or "socket_mode".

### Kwargs Injection

Listeners receive arguments by parameter name. The framework inspects function signatures and injects matching args: `body`, `event`, `action`, `command`, `payload`, `context`, `client`, `ack`, `say`, `respond`, `logger`, `complete`, `fail`, `agent`, etc. Defined in `slack_bolt/kwargs_injection/args.py`.

### Adapter System

Each adapter in `slack_bolt/adapter/` converts between a web framework's request/response types and `BoltRequest`/`BoltResponse`. Adapters exist for: Flask, FastAPI, Django, Starlette, Sanic, Bottle, Tornado, CherryPy, Falcon, Pyramid, AWS Lambda, Google Cloud Functions, Socket Mode, WSGI, ASGI, and more.

### Sync/Async Mirroring Pattern

**This is the most important pattern in this codebase.** Almost every module has both a sync and async variant. When you modify one, you almost always must modify the other.

**File naming convention:** Async files use the `async_` prefix alongside their sync counterpart:

```text
slack_bolt/middleware/custom_middleware.py          # sync
slack_bolt/middleware/async_custom_middleware.py    # async

slack_bolt/context/say/say.py                      # sync
slack_bolt/context/say/async_say.py                # async

slack_bolt/listener/custom_listener.py              # sync
slack_bolt/listener/async_listener.py              # async

slack_bolt/adapter/fastapi/async_handler.py        # async-only (no sync FastAPI adapter)
slack_bolt/adapter/flask/handler.py                # sync-only (no async Flask adapter)
```

**Which modules come in sync/async pairs:**

- `slack_bolt/app/` -- `app.py` / `async_app.py`
- `slack_bolt/middleware/` -- every middleware has an `async_` counterpart
- `slack_bolt/listener/` -- `listener.py` / `async_listener.py`, plus error/completion/start handlers
- `slack_bolt/listener_matcher/` -- `builtins.py` / `async_builtins.py`
- `slack_bolt/context/` -- each subdirectory (e.g., `say/`, `ack/`, `respond/`) has `async_` variants
- `slack_bolt/kwargs_injection/` -- `args.py` / `async_args.py`, `utils.py` / `async_utils.py`

**Adapters are an exception:** Most adapters are sync-only or async-only depending on the framework. Async-native frameworks (FastAPI, Starlette, Sanic, Tornado, ASGI, Socket Mode) have `async_handler.py`. Sync-only frameworks (Flask, Django, Bottle, CherryPy, Falcon, Pyramid, AWS Lambda, Google Cloud Functions, WSGI) have `handler.py`.

### AI Agents & Assistants

`SayStream` (`slack_bolt/context/say_stream/`) provides `chat_stream()` for AI-powered agents (experimental). `Assistant` middleware (`slack_bolt/middleware/assistant/`) handles assistant thread events. `set_status` and `set_suggested_prompts` are available as context utilities for assistant events.

## Key Development Patterns

### Adding or Modifying Middleware

1. Implement the sync version in `slack_bolt/middleware/` (subclass `Middleware`, implement `process()`)
2. Implement the async version with `async_` prefix (subclass `AsyncMiddleware`, implement `async_process()`)
3. Export built-in middleware from `slack_bolt/middleware/__init__.py` (sync) and `async_builtins.py` (async)

### Adding a Context Utility

Each context utility lives in its own subdirectory under `slack_bolt/context/`:

```text
slack_bolt/context/my_util/
    __init__.py
    my_util.py          # sync implementation
    async_my_util.py    # async implementation
    internals.py        # shared logic (optional)
```

Then wire it into `BoltContext` (`slack_bolt/context/context.py`) and `AsyncBoltContext` (`slack_bolt/context/async_context.py`).

### Adding a New Adapter

1. Create `slack_bolt/adapter/<framework>/`
2. Add `__init__.py` and `handler.py` (or `async_handler.py` for async frameworks)
3. The handler converts the framework's request to `BoltRequest`, calls `app.dispatch()`, and converts `BoltResponse` back
4. Add the framework to `requirements/adapter.txt` with version constraints
5. Add adapter tests in `tests/adapter_tests/` (or `tests/adapter_tests_async/`)

### Adding a Kwargs-Injectable Argument

1. Add the new arg to `slack_bolt/kwargs_injection/args.py` and `async_args.py`
2. Update the `Args` class with the new property
3. Populate the arg in the appropriate context or listener setup code

## Dependencies

The core package has a **single required runtime dependency**: `slack_sdk` (defined in `pyproject.toml`). Do not add runtime dependencies.

**`requirements/` directory structure:**

- `async.txt` -- async runtime deps (`aiohttp`, `websockets`)
- `adapter.txt` -- all framework adapter deps (Flask, Django, FastAPI, etc.)
- `testing.txt` -- test runner deps (`pytest`, `pytest-asyncio`, includes `async.txt`)
- `testing_without_asyncio.txt` -- test deps without async (`pytest`, `pytest-cov`)
- `adapter_testing.txt` -- adapter-specific test deps (`moto`, `boddle`, `sanic-testing`)
- `tools.txt` -- dev tools (`mypy`, `flake8`, `black`)

When adding a new dependency: add it to the appropriate `requirements/*.txt` file with version constraints, never to `pyproject.toml` `dependencies` (unless it's a core runtime dep, which is very rare).

## Test Organization

- `tests/scenario_tests/` -- Integration-style tests with realistic Slack payloads
- `tests/slack_bolt/` -- Unit tests mirroring the source structure
- `tests/adapter_tests/` and `tests/adapter_tests_async/` -- Framework adapter tests
- `tests/mock_web_api_server/` -- Mock Slack API server used by tests
- Async test variants use `_async` suffix directories

**Where to put new tests:** Mirror the source structure. For `slack_bolt/middleware/foo.py`, add tests in `tests/slack_bolt/middleware/test_foo.py`. For async variants, use the `_async` suffix directory or file naming pattern. Adapter tests go in `tests/adapter_tests/` (sync) or `tests/adapter_tests_async/` (async).

**Mock server:** Many tests use `tests/mock_web_api_server/` to simulate Slack API responses. Look at existing tests for usage patterns rather than making real API calls.

## Code Style

- **Black** formatter configured in `pyproject.toml` (line-length=125)
- **Flake8** linter configured in `.flake8` (line-length=125, ignores: F841,F821,W503,E402)
- **MyPy** configured in `pyproject.toml`
- **pytest** configured in `pyproject.toml`

## GitHub & CI/CD

- `.github/` -- GitHub-specific configuration and documentation
- `.github/workflows/` -- Continuous integration pipeline definitions that run on GitHub Actions
- `.github/maintainers_guide.md` -- Maintainer workflows and release process
