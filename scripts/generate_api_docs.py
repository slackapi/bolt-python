#!/usr/bin/env python
"""Generate the Markdown API reference for slack_bolt using griffe.

Invoked by scripts/generate_api_docs.sh. griffe (the parser behind
mkdocstrings) is used purely as the extraction engine: it loads the package,
resolves re-export aliases to their concrete definition, and parses Google-style
docstrings into structured sections. This module renders that structured data
into the Docusaurus-flavored Markdown tree the docs site imports.

The output layout (flattened under ``reference/``, package overviews as
``index.md``, an import-ready ``sidebar.json``) is produced directly rather than
rendered and then rewritten.
"""

import json
import os
import re
import shutil

import griffe

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The API reference lives under the English docs tree. DOCS_BASE_PATH is the
# directory Docusaurus doc IDs are relative to; the reference is written to
# DOCS_BASE_PATH/REFERENCE_SUBDIR.
DOCS_BASE_PATH = os.path.join(REPO_ROOT, "docs", "english")
REFERENCE_SUBDIR = "reference"

# The docs site (docs.slack.dev) imports the generated sidebar.json into its
# sidebars.js and appends it under "Bolt for Python". Its doc IDs resolve
# relative to the docs root there, hence the prefix.
SIDEBAR_DOC_ID_PREFIX = "tools/bolt-python/"

# Signatures longer than this render one parameter per line.
MAX_SIGNATURE_WIDTH = 88

PACKAGE = "slack_bolt"


# --------------------------------------------------------------------------- #
# MDX escaping
# --------------------------------------------------------------------------- #

# Docusaurus v3 parses every .md file as MDX: a bare ``<`` reads as JSX and a
# bare ``{`` as a JS expression, either of which aborts the docs build. Escape
# those two characters in prose while leaving fenced blocks and inline code
# spans untouched.
_CODE_SPLIT_RE = re.compile(r"(```[\s\S]*?```|`[^`]*`)")


def _escape_mdx(text):
    """Escape MDX-hazardous characters outside code spans and fenced blocks."""
    out = []
    for i, chunk in enumerate(_CODE_SPLIT_RE.split(text)):
        # Odd indices are the captured code spans/blocks -- leave them verbatim.
        if i % 2 == 1:
            out.append(chunk)
        else:
            out.append(chunk.replace("<", "&lt;").replace("{", "&#123;"))
    return "".join(out)


def _escape_header(name):
    """Escape a name for use in a Markdown header (underscores/asterisks)."""
    return name.replace("_", "\\_").replace("*", "\\*")


# --------------------------------------------------------------------------- #
# Signatures
# --------------------------------------------------------------------------- #

_VAR_POSITIONAL = "variadic positional"
_VAR_KEYWORD = "variadic keyword"
_POSITIONAL_ONLY = "positional-only"
_KEYWORD_ONLY = "keyword-only"


def _parameter_source(param):
    """Render a single parameter as Python source (``name: type = default``)."""
    if param.kind.value == _VAR_POSITIONAL:
        text = "*" + param.name
    elif param.kind.value == _VAR_KEYWORD:
        text = "**" + param.name
    else:
        text = param.name

    annotation = str(param.annotation) if param.annotation is not None else None
    default = str(param.default) if param.default is not None else None
    if annotation:
        text += ": " + annotation
    if default is not None and param.kind.value not in (_VAR_POSITIONAL, _VAR_KEYWORD):
        text += " = " + default if annotation else "=" + default
    return text


def _parameter_list(func, drop_first_self):
    """Build the ordered parameter fragments for a function, inserting the
    ``/`` (positional-only) and bare ``*`` (keyword-only) separators the way
    ``inspect.Signature`` does."""
    params = list(func.parameters)
    if drop_first_self and params and params[0].name in ("self", "cls"):
        params = params[1:]

    fragments = []
    render_pos_only_sep = False
    render_kw_only_sep = True
    for param in params:
        kind = param.kind.value
        if kind == _POSITIONAL_ONLY:
            render_pos_only_sep = True
        elif render_pos_only_sep:
            fragments.append("/")
            render_pos_only_sep = False

        if kind == _VAR_POSITIONAL:
            render_kw_only_sep = False
        elif kind == _KEYWORD_ONLY and render_kw_only_sep:
            fragments.append("*")
            render_kw_only_sep = False

        fragments.append(_parameter_source(param))

    if render_pos_only_sep:
        fragments.append("/")
    return fragments


def _format_function_signature(func, name, is_method):
    """Render a ``def``/``async def`` signature, wrapping long ones one
    parameter per line."""
    prefix = "async def " if "async" in (func.labels or set()) else "def "
    fragments = _parameter_list(func, drop_first_self=is_method)
    returns = " -> {}".format(func.returns) if func.returns is not None else ""

    one_line = "{}{}({}){}".format(prefix, name, ", ".join(fragments), returns)
    if len(one_line) <= MAX_SIGNATURE_WIDTH:
        return one_line

    inner = ",\n".join("    " + fragment for fragment in fragments)
    return "{}{}(\n{}){}".format(prefix, name, inner, returns)


def _format_classdef_signature(cls):
    """Render a ``class Name(bases)`` signature."""
    bases = ", ".join(str(base) for base in cls.bases)
    return "class {}({})".format(cls.name, bases)


def _property_signature(attr):
    """Render a property as a ``@property``-decorated getter."""
    returns = " -> {}".format(attr.annotation) if attr.annotation is not None else ""
    return "@property\ndef {}(){}".format(attr.name, returns)


# --------------------------------------------------------------------------- #
# Docstrings
# --------------------------------------------------------------------------- #


def _reflow_indented_code(text):
    """Convert Markdown indented code blocks (4-space, RST literal-block style
    used in many docstrings) into fenced ``python`` blocks.

    A bare indented block renders without syntax highlighting and, worse, its
    ``#`` comment lines can be misread as headers by some Markdown/MDX
    processors. Re-emitting the block fenced removes both problems and lets
    _escape_mdx leave the code verbatim. Only blocks preceded by a blank line
    are treated as code, matching CommonMark (an indented run cannot interrupt
    a paragraph)."""
    lines = text.split("\n")
    out = []
    i = 0
    prev_blank = True  # start of a section counts as a preceding blank line
    while i < len(lines):
        line = lines[i]
        if prev_blank and line.startswith("    ") and line.strip():
            block = []
            while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
                block.append(lines[i])
                i += 1
            while block and not block[-1].strip():
                block.pop()
            out.append("```python")
            out.extend(bl[4:] if bl.startswith("    ") else bl for bl in block)
            out.append("```")
            out.append("")
            prev_blank = True
            continue
        out.append(line)
        prev_blank = not line.strip()
        i += 1
    return "\n".join(out)


def _indent_continuation(text):
    """Indent wrapped continuation lines of a list item by two spaces."""
    return _escape_mdx(text).replace("\n", "\n  ")


def _render_docstring(obj, out):
    """Append an object's docstring, section by section, to ``out``."""
    if not obj.docstring:
        return
    for section in obj.docstring.parsed:
        kind = section.kind.value
        if kind == "text":
            out.append(_escape_mdx(_reflow_indented_code(section.value)))
            out.append("")
        elif kind == "parameters":
            out.append("**Arguments**:")
            out.append("")
            for param in section.value:
                typ = " _{}_".format(param.annotation) if param.annotation else ""
                if param.description:
                    out.append("- `{}`{} - {}".format(param.name, typ, _indent_continuation(param.description)))
                else:
                    out.append("- `{}`{}".format(param.name, typ))
            out.append("")
        elif kind == "returns":
            out.append("**Returns**:")
            out.append("")
            for ret in section.value:
                bits = []
                if ret.annotation:
                    bits.append("`{}`".format(ret.annotation))
                if ret.description:
                    bits.append(_indent_continuation(ret.description))
                out.append("- " + " - ".join(bits))
            out.append("")
        elif kind == "raises":
            out.append("**Raises**:")
            out.append("")
            for exc in section.value:
                typ = "`{}`".format(exc.annotation) if exc.annotation else ""
                if exc.description:
                    out.append("- {} - {}".format(typ, _indent_continuation(exc.description)))
                else:
                    out.append("- {}".format(typ))
            out.append("")
        elif kind == "admonition":
            label = (section.value.kind or "note").replace("-", " ").title()
            out.append("**{}**:".format(label))
            out.append("")
            out.append(_escape_mdx(_reflow_indented_code(section.value.contents)))
            out.append("")
        else:
            # Unknown/rare section (examples, yields, ...): render its text form.
            contents = str(getattr(section.value, "contents", section.value))
            out.append(_escape_mdx(_reflow_indented_code(contents)))
            out.append("")


# --------------------------------------------------------------------------- #
# Member selection (with re-export inlining)
# --------------------------------------------------------------------------- #


def _is_public(name):
    """Keep public names plus ``__init__`` (constructors carry the class's
    ``Args:``); drop every other dunder/private name."""
    return name == "__init__" or not name.startswith("_")


def _inlined_export_target(alias):
    """If *alias* re-exports a concrete slack_bolt class/function, return it."""
    try:
        target = alias.target
    except Exception:
        return None
    if target.canonical_path.startswith(PACKAGE + ".") and target.kind.value in ("class", "function"):
        return target
    return None


def _documented_members(parent):
    """Yield ``(display_name, object)`` pairs to document under *parent*.

    Submodules are skipped (they become their own files). Aliases are inlined
    only when they are declared in the module's ``__all__`` and resolve to a
    concrete slack_bolt class/function, so genuine public re-exports render
    inline while incidental imports do not."""
    exports = set(parent.exports or []) if parent.is_module else set()
    members = []
    for name, member in parent.members.items():
        if member.is_alias:
            if name in exports:
                target = _inlined_export_target(member)
                if target is not None:
                    members.append((name, target))
            continue
        if member.is_module:
            continue
        if not _is_public(name):
            continue
        # Drop undocumented instance attributes (bare ``self.x = x`` assignments
        # with neither a type annotation nor a docstring) -- they are
        # implementation detail. Class- and module-level constants are kept.
        labels = member.labels or set()
        if member.kind.value == "attribute" and labels == {"instance-attribute"}:
            if member.annotation is None and not member.docstring:
                continue
        members.append((name, member))
    return members


# --------------------------------------------------------------------------- #
# Object rendering
# --------------------------------------------------------------------------- #


def _render_object(display_name, obj, out):
    """Append the Markdown for a single class/function/attribute to ``out``."""
    kind = obj.kind.value

    if kind == "class":
        out.append("## {} Objects".format(_escape_header(obj.name)))
        out.append("")
        out.append("```python")
        out.append(_format_classdef_signature(obj))
        out.append("```")
        out.append("")
        _render_docstring(obj, out)
        for child_name, child in _documented_members(obj):
            _render_object(child_name, child, out)
        return

    if kind == "function":
        is_method = obj.parent is not None and obj.parent.kind.value == "class"
        out.append("#### {}".format(_escape_header(display_name)))
        out.append("")
        out.append("```python")
        out.append(_format_function_signature(obj, display_name, is_method))
        out.append("```")
        out.append("")
        _render_docstring(obj, out)
        return

    # Attribute -- a property renders as a getter, a plain variable as a header
    # carrying its type hint (no value block).
    if "property" in (obj.labels or set()):
        out.append("#### {}".format(_escape_header(display_name)))
        out.append("")
        out.append("```python")
        out.append(_property_signature(obj))
        out.append("```")
        out.append("")
    elif obj.annotation is not None:
        out.append("#### {}: `{}`".format(_escape_header(display_name), obj.annotation))
        out.append("")
    else:
        out.append("#### {}".format(_escape_header(display_name)))
        out.append("")
    _render_docstring(obj, out)


# --------------------------------------------------------------------------- #
# Module -> page
# --------------------------------------------------------------------------- #


def _relative_path(module):
    """Path of *module* relative to the top package (``""`` for slack_bolt)."""
    if module.name == PACKAGE:
        return ""
    return module.canonical_path.split(".", 1)[1].replace(".", "/")


def _iter_modules(module):
    """Yield *module* and every submodule, depth-first in source order."""
    yield module
    for member in module.members.values():
        if not member.is_alias and member.is_module:
            yield from _iter_modules(member)


def _module_docstring(module):
    """Render a module's own docstring (the package/module overview), if any."""
    out = []
    _render_docstring(module, out)
    return "\n".join(out).rstrip("\n")


def _render_body(module):
    """Render a module's members (the module docstring is rendered separately
    at the top of the page)."""
    out = []
    for name, obj in _documented_members(module):
        _render_object(name, obj, out)
    return "\n".join(out).rstrip("\n") + "\n" if out else ""


# --------------------------------------------------------------------------- #
# Routes and the sidebar
# --------------------------------------------------------------------------- #


def _doc_id(rel_path, is_package):
    """Docs-root doc ID for a module, e.g. ``reference/app/app`` or the package
    overview ``reference/app/index``."""
    if not rel_path:
        base = REFERENCE_SUBDIR + "/index"
    elif is_package:
        base = "{}/{}/index".format(REFERENCE_SUBDIR, rel_path)
    else:
        base = "{}/{}".format(REFERENCE_SUBDIR, rel_path)
    return SIDEBAR_DOC_ID_PREFIX + base


def _doc_route(doc_id):
    """Absolute Docusaurus route for a doc ID (``.../index`` served at folder)."""
    route = "/" + doc_id
    if route.endswith("/index"):
        route = route[: -len("/index")]
    return route


# --------------------------------------------------------------------------- #
# Generation
# --------------------------------------------------------------------------- #


def _load_package():
    return griffe.load(
        PACKAGE,
        search_paths=[REPO_ROOT],
        docstring_parser=griffe.Parser.google,
    )


def _build_pages(root):
    """Render every module into an in-memory page record."""
    pages = {}
    for module in _iter_modules(root):
        rel_path = _relative_path(module)
        is_package = os.path.basename(str(module.filepath)) == "__init__.py"
        dotted = module.canonical_path
        # Sidebar labels use the bare final component (e.g. "error", "app");
        # the dotted path lives in the page title instead.
        sidebar_label = dotted.rsplit(".", 1)[-1]
        pages[rel_path] = {
            "module": module,
            "is_package": is_package,
            "title": dotted,
            "sidebar_label": sidebar_label,
            "doc_id": _doc_id(rel_path, is_package),
            "docstring": _module_docstring(module),
            "body": _render_body(module),
        }
    return pages


def _submodule_links(rel_path, pages):
    """Sorted child module/subpackage links for a package overview page."""
    prefix = rel_path + "/" if rel_path else ""
    depth = prefix.count("/")
    children = []
    for other_rel, page in pages.items():
        if not other_rel or not other_rel.startswith(prefix):
            continue
        if other_rel.count("/") != depth:
            continue
        children.append((page["title"], _doc_route(page["doc_id"])))
    children.sort()
    return children


def _write_pages(pages):
    reference_dir = os.path.join(DOCS_BASE_PATH, REFERENCE_SUBDIR)
    for rel_path, page in pages.items():
        if page["is_package"] or not rel_path:
            path = os.path.join(reference_dir, rel_path, "index.md")
        else:
            path = os.path.join(reference_dir, rel_path + ".md")
        os.makedirs(os.path.dirname(path), exist_ok=True)

        frontmatter = ["---", "sidebar_label: {}".format(page["sidebar_label"]), "title: {}".format(page["title"])]
        # A module whose file is <folder>/<folder>.md collides with the folder's
        # index.md route; pin it with a relative slug.
        basename = os.path.basename(path)[: -len(".md")]
        parent = os.path.basename(os.path.dirname(path))
        if basename == parent and basename != "index":
            frontmatter.append("slug: {}".format(basename))
        frontmatter.append("---")

        body_parts = []
        if page["docstring"]:
            body_parts.append(page["docstring"])
            body_parts.append("")
        if page["is_package"] or not rel_path:
            links = _submodule_links(rel_path, pages)
            if links:
                body_parts.append("## Submodules")
                body_parts.append("")
                body_parts += ["- [{}]({})".format(title, route) for title, route in links]
                body_parts.append("")
        if page["body"]:
            body_parts.append(page["body"])

        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(frontmatter) + "\n\n" + "\n".join(body_parts).rstrip("\n") + "\n")


def _build_sidebar(pages):
    """Build the import-ready "Reference" category from the page tree."""

    def category(rel_path):
        page = pages[rel_path]
        label = page["title"].rsplit(".", 1)[-1]
        prefix = rel_path + "/" if rel_path else ""
        child_depth = prefix.count("/")

        subcategories = []
        leaves = []
        for other_rel, other in sorted(pages.items()):
            if other_rel == rel_path or not other_rel.startswith(prefix):
                continue
            if other_rel.count("/") != child_depth:
                continue
            if other["is_package"]:
                subcategories.append(category(other_rel))
            else:
                leaves.append(other["doc_id"])

        items = subcategories + leaves
        node = {"type": "category", "label": label, "link": {"type": "doc", "id": page["doc_id"]}}
        if items:
            node["items"] = items
        else:
            # No children: a plain doc leaf avoids an empty expandable node.
            return {"type": "doc", "id": page["doc_id"], "label": label}
        return node

    root = category("")
    root["label"] = "Reference"
    return root


def _write_sidebar(pages):
    sidebar = _build_sidebar(pages)
    path = os.path.join(DOCS_BASE_PATH, REFERENCE_SUBDIR, "sidebar.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(sidebar, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print("Wrote sidebar.json")


# --------------------------------------------------------------------------- #
# Safety gate + site sidebar
# --------------------------------------------------------------------------- #

_MDX_ESM_RE = re.compile(r"^(export|import)\s")


def _check_mdx_hazards():
    """Fail generation if any rendered Markdown has an MDX/acorn hazard: a line
    outside a code fence beginning with ``export``/``import`` (ESM) or ``<``
    (JSX). These come from unfenced code examples in docstrings; the fix is to
    fence the example in its source docstring."""
    reference_dir = os.path.join(DOCS_BASE_PATH, REFERENCE_SUBDIR)
    hazards = []
    for dirpath, _dirnames, filenames in os.walk(reference_dir):
        for filename in filenames:
            if not filename.endswith(".md"):
                continue
            path = os.path.join(dirpath, filename)
            in_codeblock = False
            with open(path, encoding="utf-8") as handle:
                for lineno, raw in enumerate(handle, 1):
                    line = raw.rstrip("\n")
                    if line.lstrip().startswith("```"):
                        in_codeblock = not in_codeblock
                        continue
                    if in_codeblock:
                        continue
                    if _MDX_ESM_RE.match(line) or line.startswith("<"):
                        rel = os.path.relpath(path, DOCS_BASE_PATH)
                        hazards.append("{}:{}: {}".format(rel, lineno, line))
    if hazards:
        raise SystemExit(
            "MDX/acorn hazards found in generated Markdown (unfenced code at column "
            "zero). Fence the offending example in its source docstring:\n  " + "\n  ".join(hazards)
        )
    print("No MDX/acorn hazards in generated Markdown")


def _strip_reference_from_site_sidebar():
    """Remove the "Reference" entry from docs/english/_sidebar.json.

    The reference nav is contributed by the docs-site build from
    reference/sidebar.json, so a Reference entry here too would render it twice.
    A missing entry is fine (idempotent)."""
    site_sidebar = os.path.join(DOCS_BASE_PATH, "_sidebar.json")
    with open(site_sidebar, encoding="utf-8") as handle:
        entries = json.load(handle)

    new_entries = [e for e in entries if not (isinstance(e, dict) and e.get("label") == "Reference")]
    if len(new_entries) == len(entries):
        print('No "Reference" entry in _sidebar.json to strip (already absent)')
        return

    # _sidebar.json is tab-indented; match it so the diff stays minimal.
    with open(site_sidebar, "w", encoding="utf-8") as handle:
        json.dump(new_entries, handle, indent="\t", ensure_ascii=False)
        handle.write("\n")
    print("Stripped Reference entry from _sidebar.json")


def main():
    # Rebuild the reference tree from scratch so renamed/removed modules don't
    # leave orphaned pages behind. Everything under reference/ is generated.
    reference_dir = os.path.join(DOCS_BASE_PATH, REFERENCE_SUBDIR)
    shutil.rmtree(reference_dir, ignore_errors=True)
    os.makedirs(reference_dir, exist_ok=True)
    root = _load_package()
    pages = _build_pages(root)
    _write_pages(pages)
    _write_sidebar(pages)
    _check_mdx_hazards()
    _strip_reference_from_site_sidebar()
    print("Generated {} reference pages".format(len(pages)))


if __name__ == "__main__":
    main()
