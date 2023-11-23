from unittest import mock

import pytest
from slack_bolt.cli.error import CliError
from slack_bolt.cli.get_manifest import filter_directories, find_file_path


class TestGetManifest:
    def test_filter_directories(self):
        test_directories = [
            "lib",
            "bin",
            "include",
            "src",
            "tmp",
            "test",
            "tests",
        ]

        actual = filter_directories(test_directories)

        assert actual == ["src"]

    def test_find_file_path(self):
        with mock.patch("os.walk") as mock_walk:
            mock_walk.return_value = [
                ["/dir", ["subdir"], ["utils.py", "my_app.py", "manifest.json", "app.py"]],
                ["/dir/subdir", [], ["spam.json", "hello.txt"]],
            ]

            manifest_path = find_file_path("/dir", "manifest.json")
            spam_path = find_file_path("/dir", "spam.json")

        assert manifest_path == "/dir/manifest.json"
        assert spam_path == "/dir/subdir/spam.json"

    def test_find_file_path_error(self):
        test_file_name = "test.json"

        with mock.patch("os.walk") as mock_walk:
            mock_walk.return_value = [
                ["/dir", [], ["utils.py"]],
            ]
            with pytest.raises(CliError) as e:
                find_file_path("/dir", test_file_name)

        assert str(e.value) == f"Could not find a {test_file_name} file"
