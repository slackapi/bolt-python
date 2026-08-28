"""Guard the MDX-safety invariant the API reference generator relies on.

``scripts/generate_api_docs.py`` renders every ``slack_bolt`` docstring to
Docusaurus MDX (see ``docs/english/reference``). Docusaurus v3 compiles ``.md``
as MDX, so an *unfenced* code example in a docstring is a build hazard: a line
such as ``import os`` at column zero parses as an ESM ``import`` and
``<@{user}>`` parses as JSX, either of which aborts the docs build.

The generator papers over some of this at render time -- it escapes ``<``/``{``
in prose and re-fences 4-space indented blocks -- but the durable, tool-agnostic
fix is to keep code examples fenced in the source docstring. This test enforces
that at the source: it scans every ``slack_bolt`` docstring statically with
``ast`` (no imports, so it needs no optional dependencies) and fails on an
unfenced code example or raw HTML tag.

The fix for any failure is always the same: wrap the example in a ```python
(or ```bash) fence.
"""

import ast
import os
import re

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_PACKAGE_ROOT = os.path.join(_REPO_ROOT, "slack_bolt")

_DOC_NODES = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)

# Lines that are unambiguously Python. These essentially never open a prose
# sentence, so matching one outside a code fence is a reliable "unfenced code"
# signal -- even inside a Google section such as ``Example:``.
_CODE_SIGNALS = (
    re.compile(r"^(async\s+)?def\s+\w+\s*\("),
    re.compile(r"^class\s+\w+\s*[(:]"),
    re.compile(r"^@\w[\w.]*"),
    re.compile(r"^from\s+[\w.]+\s+import\b"),
    re.compile(r"^import\s+[\w.]+(\s*,\s*[\w.]+)*(\s+as\s+\w+)?\s*$"),
)

# A line that looks like an HTML/JSX tag -- ``<div>``, ``<br/>``, ``<details>``.
# A bare ``<`` (e.g. ``count < 5``) is intentionally ignored: the generator
# escapes it harmlessly, so flagging it would only add noise.
_HTML_TAG = re.compile(r"</?[a-zA-Z][^>]*>")

# Google-style section headers. Their bodies are indented by convention, so the
# indented-block heuristic below must not mistake them for code. Code signals
# still apply inside a section, so a real example under ``Example:`` is caught.
_GOOGLE_SECTION = re.compile(
    r"^(Args|Arguments|Returns?|Yields?|Raises|Note|Notes|Example|Examples|"
    r"Attributes|Attention|Warning|Warnings|See Also|References|Todo|"
    r"Keyword Args|Keyword Arguments|Parameters)\s*:\s*$"
)


def _qualname(node):
    if isinstance(node, ast.Module):
        return "<module>"
    return node.name


def _docstring_lineno(node):
    """1-based source line of the docstring literal (for a useful failure line)."""
    first = node.body[0] if getattr(node, "body", None) else None
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
        return first.value.lineno
    return getattr(node, "lineno", 1)


def _iter_docstrings():
    """Yield ``(relpath, lineno, qualname, docstring)`` for every slack_bolt docstring."""
    for dirpath, _dirnames, filenames in os.walk(_PACKAGE_ROOT):
        for filename in sorted(filenames):
            if not filename.endswith(".py"):
                continue
            path = os.path.join(dirpath, filename)
            with open(path, encoding="utf-8") as handle:
                tree = ast.parse(handle.read(), filename=path)
            for node in ast.walk(tree):
                if not isinstance(node, _DOC_NODES):
                    continue
                docstring = ast.get_docstring(node, clean=True)
                if docstring:
                    rel = os.path.relpath(path, _REPO_ROOT)
                    yield rel, _docstring_lineno(node), _qualname(node), docstring


def _scan(docstring):
    """Return ``[(offset, line, reason)]`` for unfenced code / raw HTML in a docstring."""
    findings = []
    in_fence = False
    prev_blank = True
    in_section = False
    for offset, line in enumerate(docstring.split("\n")):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            prev_blank = False
            continue
        if in_fence:
            prev_blank = False
            continue
        if _GOOGLE_SECTION.match(stripped):
            in_section = True
            prev_blank = False
            continue
        if not stripped:
            prev_blank = True
            continue
        # A dedented (column-zero) line ends a Google section body.
        if in_section and not line.startswith((" ", "\t")):
            in_section = False
        if _HTML_TAG.search(line):
            findings.append((offset, line, "raw HTML tag"))
        if any(rx.match(stripped) for rx in _CODE_SIGNALS):
            findings.append((offset, line, "unfenced code"))
        elif prev_blank and line.startswith("    ") and not in_section:
            findings.append((offset, line, "unfenced indented code block"))
        prev_blank = False
    return findings


class TestDocstringSyntax:
    def test_code_examples_are_fenced(self):
        violations = []
        for rel, lineno, name, docstring in _iter_docstrings():
            for _offset, line, reason in _scan(docstring):
                violations.append("{}:{} ({}): {}: {}".format(rel, lineno, name, reason, line.strip()))
        assert not violations, (
            "Found unfenced code examples or raw HTML in slack_bolt docstrings. "
            "Docusaurus compiles the generated reference as MDX, so wrap each "
            "example in a ```python (or ```bash) fence:\n  " + "\n  ".join(violations)
        )

    def test_scanner_reaches_the_package(self):
        # Guard against a broken path making the fence check vacuously pass.
        count = sum(1 for _ in _iter_docstrings())
        assert count > 100, "expected to scan many docstrings, only found {}".format(count)
