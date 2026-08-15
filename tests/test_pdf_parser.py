# tests/test_pdf_parser.py

from pathlib import Path

import pytest

from research_companion.tools.pdf_parser import parse_pdf


def test_parse_pdf_file_not_found():

    with pytest.raises(FileNotFoundError):

        parse_pdf(
            "tests/fixtures/not_existing.pdf"
        )


def test_parse_pdf_invalid_file(
    tmp_path,
):

    fake_pdf = (
        tmp_path / "fake.pdf"
    )

    fake_pdf.write_text(
        "This is not a PDF.",
        encoding="utf-8",
    )

    with pytest.raises(Exception):

        parse_pdf(
            fake_pdf
        )