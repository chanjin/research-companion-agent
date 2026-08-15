# tests/unit/test_pdf_downloader.py

from pathlib import Path
from unittest.mock import patch

import pytest

from research_companion.tools.pdf_downloader import (
    build_pdf_filename,
    download_pdf,
)


class FakePdfResponse:
    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        return False

    def read(self):
        return (
            b"%PDF-1.4\n"
            b"fake pdf content"
        )


class FakeHtmlResponse:
    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        return False

    def read(self):
        return (
            b"<html>"
            b"<body>Access denied</body>"
            b"</html>"
        )


def test_build_pdf_filename_from_url():
    paper = {
        "title": "Test Paper",
    }

    result = build_pdf_filename(
        pdf_url="https://arxiv.org/pdf/2601.12345.pdf",
        paper=paper,
    )

    assert result == "2601.12345.pdf"


def test_build_pdf_filename_without_pdf_extension():
    paper = {
        "title": "Test Paper",
    }

    result = build_pdf_filename(
        pdf_url="https://arxiv.org/pdf/2601.12345",
        paper=paper,
    )

    assert result == "2601.12345.pdf"


@patch(
    "research_companion.tools.pdf_downloader.urlopen"
)
def test_download_pdf_success(
    mock_urlopen,
    tmp_path,
):
    mock_urlopen.return_value = FakePdfResponse()

    paper = {
        "title": "Test Paper",
    }

    result = download_pdf(
        pdf_url="https://example.com/test.pdf",
        paper=paper,
        output_dir=tmp_path,
    )

    path = Path(result)

    assert path.exists()
    assert path.suffix == ".pdf"

    content = path.read_bytes()

    assert content.startswith(b"%PDF")


@patch(
    "research_companion.tools.pdf_downloader.urlopen"
)
def test_download_pdf_rejects_html(
    mock_urlopen,
    tmp_path,
):
    mock_urlopen.return_value = FakeHtmlResponse()

    paper = {
        "title": "Test Paper",
    }

    with pytest.raises(
        ValueError,
        match="does not appear to be a PDF",
    ):
        download_pdf(
            pdf_url="https://example.com/test.pdf",
            paper=paper,
            output_dir=tmp_path,
        )


@patch(
    "research_companion.tools.pdf_downloader.urlopen"
)
def test_download_pdf_reuses_existing_file(
    mock_urlopen,
    tmp_path,
):
    paper = {
        "title": "Test Paper",
    }

    existing_file = (
        tmp_path / "test.pdf"
    )

    existing_file.write_bytes(
        b"%PDF-existing"
    )

    result = download_pdf(
        pdf_url="https://example.com/test.pdf",
        paper=paper,
        output_dir=tmp_path,
    )

    assert result == str(existing_file)

    mock_urlopen.assert_not_called()