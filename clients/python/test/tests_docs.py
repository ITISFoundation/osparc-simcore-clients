import pytest
import sys
import re
from pathlib import Path

_CURRENT_DIR = (
    Path(sys.argv[0] if __name__ == "__main__" else __file__).resolve().parent
)
_REPO_DIR = _CURRENT_DIR.parent.parent.parent
_DOCS_DIR = _REPO_DIR / "docs"

assert _DOCS_DIR.exists

_MD_LINK_PATTERN = re.compile(r"\[(.*?)\]\((.*?)\)")


def _collect_links():
    def _extract_file_links(markdown_file: Path) -> tuple[Path, str, str]:
        content = markdown_file.read_text()
        # Find all markdown links (e.g., [text](path/to/file))
        links = _MD_LINK_PATTERN.findall(content)
        return [(markdown_file, text, file_link) for text, file_link in links]

    links = []
    for md_file in _DOCS_DIR.rglob("*.md"):
        links.extend(_extract_file_links(md_file))
    return links


@pytest.mark.parametrize("md_file, link_text, file_link", _collect_links())
def test_markdown_links(md_file: Path, link_text: str, file_link: str):
    if file_link.startswith("http"):
        pytest.skip(f"External link skipped: {file_link}")

    # NOTE: that current doc only support relative to repo!
    relative_to_repo = (_REPO_DIR / file_link).resolve()

    assert (
        relative_to_repo.exists()
    ), f"Broken link found: [{link_text}]({file_link}) in {md_file}"
