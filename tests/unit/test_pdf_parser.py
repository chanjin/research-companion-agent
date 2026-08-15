# tests/unit/test_pdf_parser.py

from unittest.mock import patch

import pytest

from research_companion.tools.pdf_parser import (
    parse_pdf,
)


class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class FakePdfReader:
    def __init__(self, pages):
        self.pages = pages


def test_parse_pdf_file_not_found():
    with pytest.raises(
        FileNotFoundError
    ):
        parse_pdf(
            "tests/fixtures/not_existing.pdf"
        )


@patch(
    "research_companion.tools.pdf_parser.PdfReader"
)
def test_parse_pdf_success(
    mock_reader,
    tmp_path,
):
    pdf_path = (
        tmp_path / "sample.pdf"
    )

    pdf_path.write_bytes(
        b"%PDF-fake"
    )

    mock_reader.return_value = (
        FakePdfReader(
            [
                FakePage(
                    "Research Companion Agent"
                ),
                FakePage(
                    "This paper studies role boundaries."
                ),
            ]
        )
    )

    result = parse_pdf(
        pdf_path
    )

    assert (
        "Research Companion Agent"
        in result
    )

    assert (
        "role boundaries"
        in result
    )

    assert (
        "PAGE 1"
        in result
    )

    assert (
        "PAGE 2"
        in result
    )


@patch(
    "research_companion.tools.pdf_parser.PdfReader"
)
def test_parse_pdf_skips_empty_pages(
    mock_reader,
    tmp_path,
):
    pdf_path = (
        tmp_path / "sample.pdf"
    )

    pdf_path.write_bytes(
        b"%PDF-fake"
    )

    mock_reader.return_value = (
        FakePdfReader(
            [
                FakePage(None),
                FakePage("Useful content"),
            ]
        )
    )

    result = parse_pdf(
        pdf_path
    )

    assert (
        "Useful content"
        in result
    )


@patch(
    "research_companion.tools.pdf_parser.PdfReader"
)
def test_parse_pdf_no_text(
    mock_reader,
    tmp_path,
):
    pdf_path = (
        tmp_path / "sample.pdf"
    )

    pdf_path.write_bytes(
        b"%PDF-fake"
    )

    mock_reader.return_value = (
        FakePdfReader(
            [
                FakePage(None),
                FakePage(""),
            ]
        )
    )

    with pytest.raises(
        ValueError,
        match="No text could be extracted",
    ):
        parse_pdf(
            pdf_path
        )


@patch(
    "research_companion.tools.pdf_parser.PdfReader"
)
def test_parse_pdf_max_pages(
    mock_reader,
    tmp_path,
):
    pdf_path = (
        tmp_path / "sample.pdf"
    )

    pdf_path.write_bytes(
        b"%PDF-fake"
    )

    mock_reader.return_value = (
        FakePdfReader(
            [
                FakePage("Page one"),
                FakePage("Page two"),
                FakePage("Page three"),
            ]
        )
    )

    result = parse_pdf(
        pdf_path,
        max_pages=2,
    )

    assert "Page one" in result
    assert "Page two" in result
    assert "Page three" not in result