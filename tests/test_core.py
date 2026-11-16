import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from note_search.core import search, tokenize

class SearchTests(unittest.TestCase):
    def test_unicode_and_case(self):
        self.assertEqual(tokenize("CAFÉ python_3"), ["café", "python", "3"])

    def test_ranking_and_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("# Python\nPython", encoding="utf-8")
            (root / "b.md").write_text("# Other\nPython and many other words", encoding="utf-8")
            rows = search(root, "PYTHON", 1)
            self.assertEqual(rows[0]["path"], "a.md")
            self.assertEqual(rows[0]["title"], "Python")

    def test_empty_and_unmatched_queries(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(search(Path(tmp), "!!!"), [])
            self.assertEqual(search(Path(tmp), "missing"), [])

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            search(Path("missing-directory"), "query")
        with self.assertRaises(ValueError):
            search(Path("."), "query", 0)

    def test_symlink_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("python", encoding="utf-8")
            (root / "alias.md").symlink_to(root / "a.md")
            self.assertEqual(len(search(root, "python")), 1)

    def test_cli(self):
        result = subprocess.run([sys.executable, "-m", "note_search", "examples/notes", "python"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout))
