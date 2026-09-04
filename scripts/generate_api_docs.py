#!/usr/bin/env python
# Generate the Markdown API reference for slack_bolt using griffe + griffe2md.
import os
import re
import shutil

import griffe
from griffe2md import default_config, render_object_docs
from markdown_it import MarkdownIt

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_BASE_PATH = os.path.join(REPO_ROOT, "docs", "english")
REFERENCE_SUBDIR = "reference"
REFERENCE_DIR = os.path.join(DOCS_BASE_PATH, REFERENCE_SUBDIR)
SIDEBAR_DOC_ID_PREFIX = "tools/bolt-python/"

PACKAGE = "slack_bolt"

# Shared CommonMark tokenizer. Used to locate code blocks
_MD_PARSER = MarkdownIt("commonmark")


# --------------------------------------------------------------------------- #
# griffe2md rendering
# --------------------------------------------------------------------------- #

# griffe2md renders a griffe object to Markdown. 
CONFIG = dict(default_config)
CONFIG.update(
    docstring_style="google",
    summary=False,
    show_if_no_docstring=False,
    show_submodules=False,
    show_root_heading=False,
    show_root_full_path=False,
    show_root_members_full_path=False,
    show_object_full_path=False,
    heading_level=2,
    # big to keep signatures single-line, so output never depends on Black.
    line_length=10**9,
)


def _render_module(module):
    # Render a module to MDX-safe Markdown via griffe2md + post-processing.
    return _post_process(render_object_docs(module, CONFIG))


# --------------------------------------------------------------------------- #
# MDX-safety post-processing
# --------------------------------------------------------------------------- #

_CODE_SPLIT_RE = re.compile(r"(```[\s\S]*?```|`[^`]*`)")
_CODE_TAG_RE = re.compile(r"</?code>")
_ANCHOR_LINK_RE = re.compile(r"\[([^\]]+)\]\(#[^)]*\)")


def _reflow_indented_code(text):
    # Convert indented docstring code blocks into fenced ``python`` blocks.
    blocks = [t for t in _MD_PARSER.parse(text) if t.type == "code_block" and t.map]
    if not blocks:
        return text
    lines = text.split("\n")
    out = []
    cursor = 0  # 0-indexed line pointer into `lines`
    for token in blocks:
        start, end = token.map
        out.extend(lines[cursor:start])
        out.append("```python")
        out.extend(token.content.rstrip("\n").split("\n"))
        out.append("```")
        out.append("")
        cursor = end
        if cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
    out.extend(lines[cursor:])
    return "\n".join(out)


def _escape_prose(chunk):
    # Strip griffe2md markup, then escape MDX-hazardous characters in prose.
    chunk = _CODE_TAG_RE.sub("", chunk)
    chunk = _ANCHOR_LINK_RE.sub(r"\1", chunk)
    return chunk.replace("<", "&lt;").replace("{", "&#123;")


def _post_process(text):
    # Make griffe2md's Markdown safe to compile as MDX.
    text = _reflow_indented_code(text)
    out = []
    for i, chunk in enumerate(_CODE_SPLIT_RE.split(text)):
        # Odd indices are the captured code spans/blocks -- leave them verbatim.
        out.append(chunk if i % 2 else _escape_prose(chunk))
    return "".join(out).rstrip("\n")


# --------------------------------------------------------------------------- #
# Module -> page
# --------------------------------------------------------------------------- #


def _relative_path(module):
    # Path of *module* relative to the top package (``""`` for slack_bolt).
    if module.name == PACKAGE:
        return ""
    return module.canonical_path.split(".", 1)[1].replace(".", "/")


def _iter_modules(module):
    # Yield *module* and every submodule, depth-first in source order.
    yield module
    for member in module.members.values():
        if not member.is_alias and member.is_module:
            yield from _iter_modules(member)


# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #


def _doc_route(rel_path):
    base = "{}/{}".format(REFERENCE_SUBDIR, rel_path) if rel_path else REFERENCE_SUBDIR
    return "/" + SIDEBAR_DOC_ID_PREFIX + base


# --------------------------------------------------------------------------- #
# Generation
# --------------------------------------------------------------------------- #


def _load_package():
    return griffe.load(
        PACKAGE,
        search_paths=[REPO_ROOT],
        docstring_parser=griffe.Parser.google,
        resolve_aliases=True,
    )


def _build_pages(root):
    # Render every module into an in-memory page record
    pages = {}
    for module in _iter_modules(root):
        rel_path = _relative_path(module)
        pages[rel_path] = {
            "module": module,
            "is_package": module.is_init_module,
            "title": module.canonical_path,
            # griffe's module.name is the bare final component (e.g. "app").
            "sidebar_label": module.name,
            "content": _render_module(module),
        }
    return pages


def _submodule_links(rel_path, pages):
    # Sorted child module/subpackage links for a package overview page.
    prefix = rel_path + "/" if rel_path else ""
    depth = prefix.count("/")
    children = []
    for other_rel, page in pages.items():
        if not other_rel or not other_rel.startswith(prefix):
            continue
        if other_rel.count("/") != depth:
            continue
        children.append((page["title"], _doc_route(other_rel)))
    children.sort()
    return children


def _write_pages(pages):
    for rel_path, page in pages.items():
        if page["is_package"] or not rel_path:
            path = os.path.join(REFERENCE_DIR, rel_path, "index.md")
        else:
            path = os.path.join(REFERENCE_DIR, rel_path + ".md")
        os.makedirs(os.path.dirname(path), exist_ok=True)

        frontmatter = ["---", "sidebar_label: {}".format(page["sidebar_label"]), "title: {}".format(page["title"])]
        # Pin the top-level reference index to the top of its sidebar category;
        if not rel_path:
            frontmatter.append("sidebar_position: 1")
        # A module whose file is <folder>/<folder>.md collides with the folder's
        # index.md route; pin it with a relative slug.
        basename = os.path.basename(path)[: -len(".md")]
        parent = os.path.basename(os.path.dirname(path))
        if basename == parent and basename != "index":
            frontmatter.append("slug: {}".format(basename))
        frontmatter.append("---")

        body_parts = []
        if page["content"]:
            body_parts.append(page["content"])
            body_parts.append("")
        if page["is_package"] or not rel_path:
            links = _submodule_links(rel_path, pages)
            if links:
                body_parts.append("## Submodules")
                body_parts.append("")
                body_parts += ["- [{}]({})".format(title, route) for title, route in links]
                body_parts.append("")

        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(frontmatter) + "\n\n" + "\n".join(body_parts).rstrip("\n") + "\n")


# --------------------------------------------------------------------------- #
# Safety gate
# --------------------------------------------------------------------------- #

_MDX_ESM_RE = re.compile(r"^(export|import)\s")


def _code_line_numbers(text):
    # Return the set of 1-indexed line numbers that fall inside code blocks.
    covered = set()
    for token in _MD_PARSER.parse(text):
        if token.type in ("fence", "code_block") and token.map:
            start, end = token.map
            covered.update(range(start + 1, end + 1))
    return covered


def _check_mdx_hazards():
    # Fail generation if any rendered Markdown has an MDX/acorn hazard.
    hazards = []
    for dirpath, _dirnames, filenames in os.walk(REFERENCE_DIR):
        for filename in filenames:
            if not filename.endswith(".md"):
                continue
            path = os.path.join(dirpath, filename)
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            code_lines = _code_line_numbers(text)
            for lineno, line in enumerate(text.splitlines(), 1):
                if lineno in code_lines:
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


def main():
    # Rebuild the reference tree
    shutil.rmtree(REFERENCE_DIR, ignore_errors=True)
    os.makedirs(REFERENCE_DIR, exist_ok=True)
    root = _load_package()
    pages = _build_pages(root)
    _write_pages(pages)
    _check_mdx_hazards()
    print("Generated {} reference pages".format(len(pages)))


if __name__ == "__main__":
    main()
