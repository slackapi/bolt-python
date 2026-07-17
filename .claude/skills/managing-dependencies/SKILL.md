---
name: managing-dependencies
description: >-
  Use when adding, updating, pinning, or reviewing any dependency in this repo's requirements/*.txt files, including taking a Dependabot bump or writing a requirement line by hand. Also use when a pip install fails on the older Python jobs while newer ones pass, or when CI errors with "Could not find a version that satisfies", "No matching distribution found", "Requires-Python >=3.x", or "ResolutionImpossible". Triggers include: "add <package> to requirements", "bump/update <package>", "pin <package>", "fix this dependabot PR", "CI can't install <package> on Python 3.7/3.8/3.9", "requires-python error in the install step". This skill defines the layout and version-constraint conventions to follow; reach for it before hand-editing any requirements/*.txt file.
---

# Managing dependencies

## Overview

Every `requirements/*.txt` file in this repo follows one layout convention and one version-constraint pattern. This keeps a single set of pins working across the whole Python matrix and every diff readable. The mechanism for making one line behave differently per interpreter is [PEP 508](https://peps.python.org/pep-0508/) environment markers. That spec is the authority for the marker syntax used throughout this skill.

Two facts about this repo drive everything below:

- It supports **Python `>=3.7`** (`requires-python` and the classifiers in `pyproject.toml`). Its CI matrix in `.github/workflows/ci-build.yml` tests **CPython 3.7 through 3.14 only** — there is **no PyPy** (the classifiers list only `Programming Language :: Python :: Implementation :: CPython`).
- Many popular packages keep raising their minimum Python. A bump that raises a dependency's **lower bound** to a release requiring a newer Python makes pip's resolver find nothing installable on the old interpreters. The install step then fails there before tests even run.

The convention resolves this without dropping old-Python support: pin each interpreter to the newest release it can actually install, using PEP 508 `python_version` markers.

## File-layout convention

Each file starts with a `# pip install -r requirements/<file>.txt` header, then lists **one dependency per section**: the name of the dependency (as a `# name` header), an optional rationale note (starting with `# Note:`, explaining why a version is pinned or split), then the requirement line(s), separated from the next section by a blank line. This makes every pin self-documenting.

```
# pip install -r requirements/test.txt

# pytest
pytest<9.2

# pytest-cov
# Note: only needed to evaluate coverage on the latest supported python version
pytest-cov>=7.1.0,<8; python_version >= "3.14"
```

Keep this layout when adding or editing dependencies. Never leave an empty trailing `;` (a fossil of a collapsed split; delete it — the old `pytest-asyncio<2;` line was exactly this).

## Which files need Python-version markers

A marker split is only needed for requirements files installed across the **full** Python matrix. Which file you are editing decides this. To see where a file is installed, read `.github/workflows/ci-build.yml`. It is the source of truth for which Python versions install which requirements files. Everything except `dev_tools.txt` is installed by the `unittest` matrix job across 3.7–3.14.

| File                          | Installed on                                          | Needs markers?                      |
| ----------------------------- | ----------------------------------------------------- | ----------------------------------- |
| `requirements/adapter_dev.txt`  | full matrix (`unittest`; also `typecheck`/`codecov` @3.14) | **Yes, if a bump raises the floor** |
| `requirements/async_dev.txt`     | full matrix (`unittest`; also `typecheck`/`codecov` @3.14) | **Yes, if a bump raises the floor** |
| `requirements/test.txt`          | full matrix (`unittest`)                              | **Yes, if a bump raises the floor** |
| `requirements/test_adapter.txt`  | full matrix (`unittest`; `codecov` @3.14)             | **Yes, if a bump raises the floor** |
| `requirements/test_async.txt`    | full matrix (`unittest`)                              | **Yes, if a bump raises the floor** |
| `requirements/dev_tools.txt`     | `lint` + `typecheck`, **latest Python only** (3.14)   | No, just take the bump (`==` pins)  |

If the bump lands in a latest-Python-only file, take it as-is: no markers, no ceiling, just the layout convention above.

Unlike some sibling repos, bolt-python has **no requirements file that feeds packaged wheel metadata**: `pyproject.toml` has no `[project.optional-dependencies]`, and `[tool.setuptools.dynamic]` resolves only `version` and `readme`. So there is no "special" file whose comments leak into a wheel — every `requirements/*.txt` file is dev/test-only.

## The version-constraint pattern

When a dependency's floor rises to a release that requires a newer Python, **do not** just take the bump, and **do not** drop old-Python support to make CI pass. Instead, split the requirement into `python_version`-marked lines that **partition the whole matrix**. Every interpreter matches exactly one line. Old interpreters keep the last compatible release (with an explicit ceiling), and the newest line is open-ended so future Pythons stay covered.

```
# aiohttp
aiohttp>=3,<4; python_version < "3.9"
aiohttp>=3.13.5,<4; python_version >= "3.9"
```

`aiohttp` 3.13.5 requires Python `>=3.9`, so Python 3.7/3.8 stay on the older line. The same 3.9 split appears for `falcon`, `fastapi`, `Flask`, `Werkzeug`, `starlette`, `tornado`, `websocket_client`, and (in `test_async.txt`) `asgiref`. The `Django` split lands at 3.8 instead — Django 4.x requires `>=3.8`, so 3.7 keeps the 3.2 line:

```
# Django
Django>=3.2,<4; python_version < "3.8"
Django>=4.2.30,<6; python_version >= "3.8"
```

## Canonical marker style

Consistency matters because these lines are read and edited often, and a stray style makes diffs noisy. Standardize on this:

- Spaces around every operator in the marker: `python_version >= "3.9"`, never `python_version>="3.9"`.
- Double-quoted `major.minor` string: `"3.9"`. (`packaging` compares these version-aware, so `python_version >= "3.9"` correctly includes 3.10–3.14, no lexicographic surprise.)
- Use `>=` / `<` for the Python boundary; avoid `>` / `<=` so the boundary version lands on exactly one side. **This rule is about the `python_version` marker, not the version specifier** — `boto3<=2` and `cheroot<12` are correct as written.
- One space after the `;`, none before: `pkg>=1,<2; python_version >= "3.9"`.
- The old-side line always carries an explicit upper bound (the floor-jump version).
- The marker set must be **exhaustive and mutually exclusive** across the matrix. The newest line ends open-ended (`>= "X.Y"`), never a bare `==` that leaves future Pythons unmatched.

## Deriving the versions to pin

You need two numbers: the **floor** (which Python the new release requires) and the old-side **ceiling** (the first release that raised that floor).

1. **Floor.** Read the metadata for the _exact target version_ at `https://pypi.org/pypi/<package>/<target-version>/json`. The `info.requires_python` field gives the new minimum (e.g. `">=3.9"`). A `null` there means the release declares no floor.

2. **Ceiling.** Walk the release history at `https://pypi.org/pypi/<package>/json` and find the **first version that raised the floor above the oldest matrix Python**. The old-side ceiling is `< <that version>`. For example, if a package jumped to `>=3.9` at version **4.0.0**, the old-side cap is `<4` even if the target is `4.2.0` (pinning `<4.2.0` would wrongly admit 4.0.0–4.1.x, which are also 3.9-only).

Why an explicit ceiling instead of trusting pip to filter by `Requires-Python`? Because that filtering only holds if every future release keeps its metadata correct; a single mis-tagged release would silently float onto an untested interpreter. An explicit ceiling makes the intent self-documenting and robust.

`tracerite` is the cautionary case: its releases after 1.1.2 break on Python `<= 3.8`, yet those releases publish **no `requires_python` metadata at all** (verify: `https://pypi.org/pypi/tracerite/1.1.3/json` shows `requires_python: null`). So pip filtering offers zero protection on the old interpreters, and the explicit `tracerite<1.1.2` ceiling is load-bearing, not decorative.

**If you arrived here from a red CI job:** the failing _install_ log is ground truth. It names the interpreter that failed and the versions pip was actually offered, e.g.:

```
ERROR: Ignored the following versions that require a different python version: 4.2.0 Requires-Python >=3.9
ERROR: Could not find a version that satisfies the requirement falcon>=4.2.0 (from versions: ..., 3.1.3)
```

Cross-check the PyPI value against that log so you are never guessing. (If instead the failure is a real test failure, or hits _every_ Python version, this pattern does not apply, so investigate the bump normally.)

## One harder shape: a coupled companion dependency

Sometimes a package drags in another distribution with loose or wildcard versions that you must co-pin on the same boundary. `Sanic` imports `tracerite` with wildcard versions, so `tracerite` is pinned right beside it:

```
# sanic
# Note: Sanic pulls in tracerite via a wildcard version, so tracerite is co-pinned here.
# Note: tracerite > 1.1.2 is incompatible with Python <= 3.8 and ships no requires_python, so an explicit ceiling is required.
tracerite<1.1.2; python_version < "3.9"
sanic>=21,<24; python_version < "3.9"
sanic>=25.3.0,<26; python_version >= "3.9"
```

The split boundary here (3.9) is driven by `tracerite`, **not** by Sanic itself — Sanic 25.3 supports Python 3.8 (`requires_python: >=3.8`). Python 3.8 is kept on old Sanic only because tracerite breaks there. When a companion transitive dependency is the thing that breaks, pin it explicitly rather than hoping the parent's resolver picks a compatible version, and keep it in the same section so the coupling stays visible.

## Collapse when a Python is dropped

Marker splits are maintenance cost, so remove them when they stop earning their keep. When a Python version is dropped from the CI matrix (and from `requires-python` / the classifiers), collapse any split whose only reason was that version back into a single unmarked line, and delete the trailing `;`. For example, if 3.7 is dropped, the `Django>=3.2,<4; python_version < "3.8"` line has no interpreter left to serve, and the section collapses to a single `Django` line. A leaner file is easier for both humans and Dependabot to reason about.

## What to leave alone

- **Do not touch `requires-python` or the CI matrix.** Keeping 3.7 working on old dependency versions is the entire point; changing the floor is a separate, deliberate decision.
- **Do not add runtime dependencies to `pyproject.toml`.** The core package depends only on `slack_sdk` (see the "Single Runtime Dependency Rule" in `AGENTS.md`); everything else belongs in `requirements/*.txt`.
- **Prefer markers over a Dependabot `ignore`.** An `ignore` rule freezes newer Pythons on the old version too, and hides the version knowledge in config. Reserve `ignore` for the rare dep that must stay pinned everywhere for reproducible output.
