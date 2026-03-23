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

You can verify the venv is active by checking `echo $VIRTUAL_ENV`. If tools like `black`, `flake8`, `mypy` or `pytest` are not found, ask the user to activate the venv.

A python virtual environment (`venv`) should be activated before running any commands.

```bash
# Create a venv (first time only)
python -m venv .venv

# Activate
source .venv/bin/activate

# Install all dependencies
./scripts/install.sh
```

## Common Commands

### Pre-submission Checklist

Before considering any work complete, you MUST run these commands in order and confirm they all pass:

```bash
./scripts/format.sh --no-install     # 1. Format
./scripts/lint.sh --no-install        # 2. Lint
./scripts/run_tests.sh <relevant>     # 3. Run relevant tests (see Testing below)
./scripts/run_mypy.sh --no-install    # 4. Type check
```

To run everything at once (installs deps + formats + lints + tests + typechecks):

```bash
./scripts/install_all_and_run_tests.sh
```

### Testing

Always use the project scripts instead of calling `pytest` directly:

```bash
# Run a single test file
./scripts/run_tests.sh tests/scenario_tests/test_app.py

# Run a single test function
./scripts/run_tests.sh tests/scenario_tests/test_app.py::TestApp::test_name
```

### Formatting, Linting, Type Checking

```bash
# Format -- Black, configured in pyproject.toml
./scripts/format.sh --no-install

# Lint -- Flake8, configured in .flake8
./scripts/lint.sh --no-install

# Type check -- mypy, configured in pyproject.toml
./scripts/run_mypy.sh --no-install
```

## Critical Conventions

### Sync/Async Mirroring Rule

**When modifying any sync module, you MUST also update the corresponding async module (and vice versa).** This is the most important convention in this codebase.

Almost every module has both a sync and async variant. Async files use the `async_` prefix alongside their sync counterpart:

```text
slack_bolt/middleware/custom_middleware.py          # sync
slack_bolt/middleware/async_custom_middleware.py    # async

slack_bolt/context/say/say.py                      # sync
slack_bolt/context/say/async_say.py                # async

slack_bolt/listener/custom_listener.py              # sync
slack_bolt/listener/async_listener.py              # async
```

**Modules that come in sync/async pairs:**

- `slack_bolt/app/` -- `app.py` / `async_app.py`
- `slack_bolt/middleware/` -- every middleware has an `async_` counterpart
- `slack_bolt/listener/` -- `listener.py` / `async_listener.py`, plus error/completion/start handlers
- `slack_bolt/listener_matcher/` -- `builtins.py` / `async_builtins.py`
- `slack_bolt/context/` -- each subdirectory (e.g., `say/`, `ack/`, `respond/`) has `async_` variants
- `slack_bolt/kwargs_injection/` -- `args.py` / `async_args.py`, `utils.py` / `async_utils.py`

**Adapters are an exception:** Most adapters are sync-only or async-only depending on the framework. Async-native frameworks (FastAPI, Starlette, Sanic, Tornado, ASGI, Socket Mode) have `async_handler.py`. Sync-only frameworks (Flask, Django, Bottle, CherryPy, Falcon, Pyramid, AWS Lambda, Google Cloud Functions, WSGI) have `handler.py`.

### Prefer the Middleware Pattern

Middleware is the project's preferred approach for cross-cutting concerns. Before adding logic to individual listeners or utility functions, consider whether it belongs as a built-in middleware in the framework.

**When to add built-in middleware:**

- Cross-cutting concerns that apply to many or all requests (logging, metrics, observability)
- Request validation, transformation, or enrichment
- Authorization extensions beyond the built-in `SingleTeamAuthorization`/`MultiTeamsAuthorization`
- Feature-level request handling (the `Assistant` middleware in `slack_bolt/middleware/assistant/assistant.py` is the canonical example -- it intercepts assistant thread events and dispatches them to registered sub-listeners)

**How to add built-in middleware:**

1. Subclass `Middleware` (sync) and implement `process(self, *, req, resp, next)`. Call `next()` to continue the chain.
2. Subclass `AsyncMiddleware` (async) and implement `async_process(self, *, req, resp, next)`. Call `await next()` to continue.
3. Export from `slack_bolt/middleware/__init__.py` (sync) and `slack_bolt/middleware/async_builtins.py` (async).
4. Register the middleware in `App.__init__()` (`slack_bolt/app/app.py`) and `AsyncApp.__init__()` (`slack_bolt/app/async_app.py`) where the default middleware chain is assembled.

**Canonical example:** `AttachingFunctionToken` (`slack_bolt/middleware/attaching_function_token/`) is a good small middleware to follow -- it has a clean sync/async pair, a focused `process()` method, and is properly exported and registered in the app's middleware chain.

### Single Runtime Dependency Rule

The core package depends ONLY on `slack_sdk` (defined in `pyproject.toml`). Never add runtime dependencies to `pyproject.toml`. Additional dependencies go in the appropriate `requirements/*.txt` file.

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

Listeners receive arguments by parameter name. The framework inspects function signatures and injects matching args: `body`, `event`, `action`, `command`, `payload`, `context`, `client`, `ack`, `say`, `respond`, `logger`, `complete`, `fail`, etc. Defined in `slack_bolt/kwargs_injection/args.py`.

### Adapter System

Each adapter in `slack_bolt/adapter/` converts between a web framework's request/response types and `BoltRequest`/`BoltResponse`. Adapters exist for: Flask, FastAPI, Django, Starlette, Sanic, Bottle, Tornado, CherryPy, Falcon, Pyramid, AWS Lambda, Google Cloud Functions, Socket Mode, WSGI, ASGI, and more.

### AI Agents & Assistants

`Assistant` middleware (`slack_bolt/middleware/assistant/`) handles assistant thread events.

## Key Development Patterns

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
5. Add adapter tests in `tests/adapter_tests/` (sync) or `tests/adapter_tests_async/` (async)

### Adding a Kwargs-Injectable Argument

1. Add the new arg to `slack_bolt/kwargs_injection/args.py` and `async_args.py`
2. Update the `Args` class with the new property
3. Populate the arg in the appropriate context or listener setup code

## Security Considerations

- **Request Verification:** The built-in `RequestVerification` middleware validates `x-slack-signature` and `x-slack-request-timestamp` on every incoming HTTP request. Never disable this in production. It is automatically skipped for `socket_mode` requests.
- **Tokens & Secrets:** `SLACK_SIGNING_SECRET` and `SLACK_BOT_TOKEN` must come from environment variables. Never hardcode or commit secrets.
- **Authorization Middleware:** `SingleTeamAuthorization` and `MultiTeamsAuthorization` verify tokens and inject an authorized `WebClient` into the context. Do not bypass these.
- **Tests:** Always use mock servers (`tests/mock_web_api_server/`) and dummy values. Never use real tokens in tests.

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

## Test Organization and CI

### Directory Structure

- `tests/scenario_tests/` -- Integration-style tests with realistic Slack payloads
- `tests/slack_bolt/` -- Unit tests mirroring the source structure
- `tests/adapter_tests/` and `tests/adapter_tests_async/` -- Framework adapter tests
- `tests/mock_web_api_server/` -- Mock Slack API server used by tests
- Async test variants use `_async` suffix directories

**Where to put new tests:** Mirror the source structure. For `slack_bolt/middleware/foo.py`, add tests in `tests/slack_bolt/middleware/test_foo.py`. For async variants, use the `_async` suffix directory or file naming pattern. Adapter tests go in `tests/adapter_tests/` (sync) or `tests/adapter_tests_async/` (async).

**Mock server:** Many tests use `tests/mock_web_api_server/` to simulate Slack API responses. Look at existing tests for usage patterns rather than making real API calls.

### CI Pipeline

GitHub Actions (`.github/workflows/ci-build.yml`) runs on every push to `main` and every PR:

- **Lint** -- `./scripts/lint.sh` on latest Python
- **Typecheck** -- `./scripts/run_mypy.sh` on latest Python
- **Unit tests** -- full test suite across Python 3.7--3.14 matrix
- **Code coverage** -- uploaded to Codecov

## PR and Commit Guidelines

- PRs target the `main` branch
- You MUST run `./scripts/install_all_and_run_tests.sh` before submitting
- PR template (`.github/pull_request_template.md`) requires: Summary, Testing steps, Category checkboxes (`App`, `AsyncApp`, Adapters, Docs, Others)
- Requirements: CLA signed, test suite passes, code review approval
- Commits should be atomic with descriptive messages. Reference related issue numbers.
