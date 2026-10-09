import importlib.util
import os

import pytest

_SCRIPT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "scripts",
    "generate_api_docs.py",
)


@pytest.fixture(scope="module")
def gen():
    spec = importlib.util.spec_from_file_location("generate_api_docs", _SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestReflowIndentedCode:
    def test_indented_block_becomes_fenced_python(self, gen):
        text = "Example:\n\n    x = 1\n    y = 2\n\nDone.\n"
        assert gen._reflow_indented_code(text) == ("Example:\n\n```python\nx = 1\ny = 2\n```\n\nDone.\n")

    def test_existing_fence_is_left_untouched(self, gen):
        text = "Intro\n\n```python\nx = 1\n```\n\nOutro\n"
        assert gen._reflow_indented_code(text) == text

    def test_list_continuation_is_not_treated_as_code(self, gen):
        # A 4-space indent under a list item is list content in CommonMark, not
        # an indented code block; it must not be fenced.
        text = "- first\n\n    still the first item\n\n- second\n"
        assert gen._reflow_indented_code(text) == text

    def test_prose_without_code_is_unchanged(self, gen):
        text = "Just a paragraph.\n\nAnd another one.\n"
        assert gen._reflow_indented_code(text) == text

    def test_trailing_blank_line_is_not_duplicated(self, gen):
        result = gen._reflow_indented_code("A\n\n    code()\n\nB\n")
        assert "\n\n\n" not in result


class TestEscapeProse:
    def test_angle_and_brace_are_escaped_in_prose(self, gen):
        assert gen._escape_prose("Optional<str> and {value}") == "Optional&lt;str> and &#123;value}"

    def test_code_wrapper_and_anchor_links_are_stripped(self, gen):
        assert gen._escape_prose("<code>[App](#slack_bolt.App)</code>") == "App"

    def test_real_url_links_are_preserved(self, gen):
        text = "see [docs](https://example.com/x)"
        assert gen._escape_prose(text) == text


class TestDocRoute:
    def test_root_route_has_no_rel_path(self, gen):
        assert gen._doc_route("") == "/tools/bolt-python/reference"

    def test_package_and_module_routes_append_rel_path(self, gen):
        # Index pages are served at their folder, so a package and a plain
        # module produce the same shape of route -- just the rel_path appended.
        assert gen._doc_route("app") == "/tools/bolt-python/reference/app"
        assert gen._doc_route("app/app") == "/tools/bolt-python/reference/app/app"


class TestPostProcess:
    def test_code_spans_and_blocks_stay_verbatim(self, gen):
        text = "Use `Optional<str>` inline.\n\n```python\nx: Optional[int] = {1}\n```\n"
        result = gen._post_process(text)
        assert "`Optional<str>`" in result
        assert "x: Optional[int] = {1}" in result

    def test_prose_hazards_outside_code_are_escaped(self, gen):
        result = gen._post_process("A value like <T> or {k}.\n")
        assert "&lt;T> or &#123;k}" in result
