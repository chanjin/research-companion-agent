# src/research_companion/tools/pdf_parser.py

from pathlib import Path

from pypdf import PdfReader


def parse_pdf(
    pdf_path: str | Path,
    max_pages: int | None = None,
) -> str:
    """
    PDF에서 텍스트를 추출한다.

    Parameters
    ----------
    pdf_path:
        PDF 파일 경로.

    max_pages:
        읽을 최대 페이지 수.
        None이면 전체 페이지를 읽는다.

    Returns
    -------
    str
        PDF에서 추출된 텍스트.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {path}"
        )

    reader = PdfReader(
        str(path)
    )

    page_texts = []

    pages = reader.pages

    if max_pages is not None:
        pages = pages[:max_pages]

    for page_number, page in enumerate(
        pages,
        start=1,
    ):

        text = page.extract_text()

        if not text:
            continue

        page_texts.append(
            (
                f"\n\n"
                f"===== PAGE {page_number} =====\n\n"
                f"{text.strip()}"
            )
        )

    paper_text = "".join(
        page_texts
    ).strip()

    if not paper_text:
        raise ValueError(
            "No text could be extracted from the PDF."
        )

    return paper_text