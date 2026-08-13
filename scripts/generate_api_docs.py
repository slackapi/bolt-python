#!/usr/bin/env python
"""Generate the Markdown API reference for slack_bolt using pydoc-markdown.

This is invoked by scripts/generate_api_docs.sh. It exists as a Python driver
(rather than a plain `pydoc-markdown` CLI call) because pydoc-markdown has no
built-in way to inline re-exported objects: by default a module that only
re-exports a class (e.g. slack_bolt/adapter/fastapi/__init__.py re-exporting
SlackRequestHandler from the starlette adapter) renders as an empty page, and
the class is documented only at its definition site.

pdoc3 (the previous generator) inlined re-exports at every re-export site, so
framework-specific pages such as adapter/fastapi showed their handler class.
To preserve that behavior, inline_reexports() resolves each re-export to the
concrete Class/Function and splices a copy in under the exported name.
"""

import copy
import html
import json
import os
import re

import docspec
from pydoc_markdown import PydocMarkdown
from pydoc_markdown.contrib.processors.google import GoogleProcessor, generate_sections_markdown
from pydoc_markdown.contrib.processors.smart import SmartProcessor
from pydoc_markdown.contrib.renderers import markdown as _markdown_renderer

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _escape_except_code(string):
    """HTML-escape a docstring while leaving fenced blocks and inline code spans
    untouched.

    This replaces pydoc-markdown's own ``escape_except_blockquotes``, which has a
    token-collision bug: it swaps each code span for a ``BLOCKQUOTE_TOKEN_<i>``
    placeholder and later restores them with ``str.replace``. Once a docstring has
    more than ten code spans, restoring ``BLOCKQUOTE_TOKEN_1`` also rewrites the
    ``BLOCKQUOTE_TOKEN_1`` prefix of ``BLOCKQUOTE_TOKEN_10``/``_11``/..., which
    duplicates whatever token 1 held (often a whole fenced code block) into later
    spans and leaves stray ``0``/``1`` digits behind. Bolt's ``App.step`` docstring
    (a fenced example plus a many-item ``Args:`` list) triggers exactly this.

    The fix uses NUL-delimited placeholders so no placeholder is a prefix of
    another, and restores each exactly once.
    """
    triple = r"```[\s\S]*?```"
    single = r"`[^`]*`"
    matches = re.findall("({}|{})".format(triple, single), string)
    for i, match in enumerate(matches):
        string = string.replace(match, "\x00CODE{}\x00".format(i), 1)
    escaped = html.escape(string)
    for i, match in enumerate(matches):
        escaped = escaped.replace("\x00CODE{}\x00".format(i), match, 1)
    return escaped


CONFIG = {
    "loaders": [
        {"type": "python", "search_path": [REPO_ROOT], "packages": ["slack_bolt"]},
    ],
    "processors": [
        # documented_only=False keeps signatures for members that lack a
        # docstring (matching pdoc3). The expression drops private names and
        # Indirection members (bare imports/re-exports) so imported symbols
        # like Optional/WebClient do not leak in as empty headings.
        {
            "type": "filter",
            "documented_only": False,
            "exclude_private": True,
            "expression": ('not name.startswith("_") and default() ' 'and obj.__class__.__name__ != "Indirection"'),
        },
        {"type": "smart"},
        {"type": "crossref"},
    ],
    "renderer": {
        "type": "docusaurus",
        "docs_base_path": os.path.join(REPO_ROOT, "docs"),
        "relative_output_path": "reference",
    },
}


class OrderedGoogleProcessor(GoogleProcessor):
    """GoogleProcessor that keeps fenced code blocks in their original position.

    The stock GoogleProcessor buffers every line into ``current_lines`` and only
    flushes it when a section keyword (``Args:`` etc.) is reached. A fenced code
    block that appears *before* any section keyword therefore gets held back and
    re-emitted after the intervening prose, leaving a blank gap where it was.
    bolt-python docstrings routinely show a usage example first and then prose,
    so this reorders them. This override sends pre-keyword lines (including code
    fences) straight to the output so their order is preserved, while keeping the
    stock Google-style ``Args:`` -> ``**Arguments**`` section rendering.
    """

    def _process(self, node):
        if not node.docstring:
            return
        lines = []
        current_lines = []
        in_codeblock = False
        keyword = None

        def _commit():
            if keyword:
                generate_sections_markdown(lines, {keyword: current_lines})
            else:
                lines.extend(current_lines)
            current_lines.clear()

        for line in node.docstring.content.split("\n"):
            if line.lstrip().startswith("```"):
                in_codeblock = not in_codeblock
                (current_lines if keyword else lines).append(line)
                continue

            if in_codeblock:
                (current_lines if keyword else lines).append(line)
                continue

            line = line.strip()
            if line in self._keywords_map:
                _commit()
                keyword = self._keywords_map[line]
                continue

            if keyword is None:
                lines.append(line)
                continue

            param_match = None
            for param_re in self._param_res:
                param_match = param_re.match(line)
                if param_match:
                    groups = param_match.groupdict()
                    if "type" in groups:
                        current_lines.append("- `{param}` _{type}_ - {desc}".format(**groups))
                    else:
                        current_lines.append("- `{param}` - {desc}".format(**groups))
                    break

            if not param_match:
                current_lines.append("  {line}".format(line=line))

        _commit()
        node.docstring.content = "\n".join(lines)


def _use_ordered_google_processor(session):
    """Swap the stock GoogleProcessor inside the `smart` processor for the
    order-preserving subclass above."""
    for processor in session.processors:
        if isinstance(processor, SmartProcessor):
            processor.google = OrderedGoogleProcessor()


def _build_index(modules):
    """Map every member's fully-qualified name to its docspec object, and
    return the set of names that are packages (have submodules)."""
    index = {}
    module_names = set()

    def visit(obj, prefix):
        fqn = "{}.{}".format(prefix, obj.name) if prefix else obj.name
        index[fqn] = obj
        for child in getattr(obj, "members", None) or []:
            visit(child, fqn)

    for mod in modules:
        module_names.add(mod.name)
        visit(mod, "")

    packages = {
        name for name in module_names if any(other != name and other.startswith(name + ".") for other in module_names)
    }
    return index, packages


def _resolve_target(target, module_name, packages):
    """Resolve a relative Indirection target to an absolute FQN using Python
    import semantics. For a package __init__, one leading dot is the package
    itself; for a regular module it is the containing package."""
    if not target.startswith("."):
        return target
    dots = len(target) - len(target.lstrip("."))
    rest = target[dots:]
    containing_pkg = module_name if module_name in packages else module_name.rsplit(".", 1)[0]
    up = dots - 1
    base_parts = containing_pkg.split(".")
    base = base_parts[: len(base_parts) - up] if up else base_parts
    return ".".join(base + ([rest] if rest else [])) if base else rest


def _follow(fqn, index, packages, seen):
    """Follow an indirection chain to the concrete Class/Function, or None."""
    if fqn in seen:
        return None
    seen.add(fqn)
    obj = index.get(fqn)
    if obj is None:
        return None
    if isinstance(obj, (docspec.Class, docspec.Function)):
        return obj
    if type(obj).__name__ == "Indirection":
        parent = fqn.rsplit(".", 1)[0]
        return _follow(_resolve_target(obj.target, parent, packages), index, packages, seen)
    return None


def inline_reexports(modules):
    """Replace re-export Indirections with a copy of the object they point to,
    so re-export-only modules render the class/function inline."""
    index, packages = _build_index(modules)
    inlined = 0
    for mod in modules:
        new_members = []
        for member in mod.members:
            if type(member).__name__ == "Indirection":
                fqn = _resolve_target(member.target, mod.name, packages)
                target_obj = _follow(fqn, index, packages, set())
                if target_obj is not None:
                    clone = copy.deepcopy(target_obj)
                    clone.name = member.name
                    new_members.append(clone)
                    inlined += 1
                    continue
            new_members.append(member)
        mod.members = new_members
    print("Inlined {} re-exported objects".format(inlined))


def main():
    # The docusaurus renderer writes sidebar.json into the output directory and
    # expects it to already exist.
    os.makedirs(os.path.join(REPO_ROOT, "docs", "reference"), exist_ok=True)

    # Replace pydoc-markdown's buggy code-span-preserving HTML escaper (see
    # _escape_except_code for the bug it fixes). The MarkdownRenderer looks the
    # function up on its own module at render time, so patching it here is enough.
    _markdown_renderer.escape_except_blockquotes = _escape_except_code

    session = PydocMarkdown()
    session.load_config(CONFIG)
    _use_ordered_google_processor(session)
    modules = session.load_modules()
    inline_reexports(modules)
    session.process(modules)
    session.render(modules)
    _rename_package_indexes()


def _rename_package_indexes():
    """Rename each package's ``__init__.md`` to ``index.md`` and rewrite the
    generated ``sidebar.json`` to match.

    The docusaurus renderer writes a package's docs to ``<pkg>/__init__.md``,
    whose Docusaurus route is ``.../<pkg>/__init__`` -- there is no document at
    the bare ``.../<pkg>/`` URL. Docusaurus serves ``index.md`` at the folder
    URL, so renaming makes ``.../reference/slack_bolt/`` resolve (the path the
    sidebar's Reference link points at) instead of 404ing.
    """
    reference_dir = os.path.join(REPO_ROOT, "docs", "reference")
    renamed = 0
    for dirpath, _dirnames, filenames in os.walk(reference_dir):
        if "__init__.md" in filenames:
            os.replace(
                os.path.join(dirpath, "__init__.md"),
                os.path.join(dirpath, "index.md"),
            )
            renamed += 1

    sidebar_path = os.path.join(reference_dir, "sidebar.json")
    with open(sidebar_path, encoding="utf-8") as handle:
        sidebar = json.load(handle)

    def rewrite(node):
        if isinstance(node, str):
            return node[: -len("__init__")] + "index" if node.endswith("/__init__") else node
        if isinstance(node, list):
            return [rewrite(item) for item in node]
        if isinstance(node, dict):
            return {key: rewrite(value) for key, value in node.items()}
        return node

    with open(sidebar_path, "w", encoding="utf-8") as handle:
        json.dump(rewrite(sidebar), handle, indent=2)
        handle.write("\n")

    print("Renamed {} package __init__.md files to index.md".format(renamed))


if __name__ == "__main__":
    main()
