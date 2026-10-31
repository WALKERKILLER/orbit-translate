"""Docs gate: llms.txt index closure and resolvable relative links and images."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

from tests.support import ROOT

_WIKI = ROOT / "llms-wiki"
_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)|\bsrc=\"([^\"]+)\"")
_DOCS = ("README.md", "README.zh-CN.md", "AGENTS.md", "CHANGELOG.md")


def _local_targets(path: Path):
    for match in _LINK.finditer(path.read_text(encoding="utf-8")):
        target = match.group(1) or match.group(2)
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        yield target.split("#", 1)[0]


class DocsGateTests(unittest.TestCase):
    def test_llms_index_lists_every_wiki_page_and_nothing_else(self) -> None:
        indexed = {
            (_WIKI / target).resolve()
            for target in _local_targets(_WIKI / "llms.txt")
            if target.endswith(".md") and not target.startswith("../")
        }
        pages = {path.resolve() for path in _WIKI.glob("*.md")}
        self.assertEqual(indexed, pages)

    def test_relative_links_resolve(self) -> None:
        files = [ROOT / name for name in _DOCS] + sorted(_WIKI.glob("*"))
        for path in files:
            for target in _local_targets(path):
                with self.subTest(file=path.name, link=target):
                    self.assertTrue((path.parent / target).exists())

    def test_agents_stays_short(self) -> None:
        self.assertLessEqual(len((ROOT / "AGENTS.md").read_text(encoding="utf-8").splitlines()), 150)


if __name__ == "__main__":
    unittest.main()
