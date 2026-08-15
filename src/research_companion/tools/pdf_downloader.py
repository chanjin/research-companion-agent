# src/research_companion/tools/pdf_downloader.py

from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse


DEFAULT_PAPER_DIR = Path("data/papers")


def build_pdf_filename(
    pdf_url: str,
    paper: dict,
) -> str:
    """
    PDF 저장 파일명을 생성한다.

    arXiv URL에서 가능한 경우 arXiv ID를 사용하고,
    그렇지 않으면 논문 제목 일부를 이용한다.
    """

    parsed = urlparse(pdf_url)

    path_name = Path(parsed.path).name

    if path_name:
        arxiv_id = path_name.replace(".pdf", "")

        if arxiv_id:
            return f"{arxiv_id}.pdf"

    title = paper.get(
        "title",
        "paper",
    )

    safe_title = "".join(
        character
        if character.isalnum()
        else "_"
        for character in title
    )

    safe_title = safe_title[:80].strip("_")

    if not safe_title:
        safe_title = "paper"

    return f"{safe_title}.pdf"


def download_pdf(
    pdf_url: str,
    paper: dict,
    output_dir: str | Path = DEFAULT_PAPER_DIR,
) -> str:
    """
    논문 PDF를 다운로드한다.

    Parameters
    ----------
    pdf_url:
        다운로드할 PDF URL.

    paper:
        논문의 metadata.

    output_dir:
        PDF 저장 디렉터리.

    Returns
    -------
    str
        저장된 PDF 파일 경로.
    """

    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = build_pdf_filename(
        pdf_url=pdf_url,
        paper=paper,
    )

    file_path = output_path / filename

    # 이미 다운로드되어 있으면 다시 받지 않는다.
    if file_path.exists():
        return str(file_path)

    request = Request(
        pdf_url,
        headers={
            "User-Agent": (
                "ResearchCompanionAgent/0.1 "
                "(academic research project)"
            )
        },
    )

    with urlopen(
        request,
        timeout=30,
    ) as response:

        content = response.read()

    if not content.startswith(b"%PDF"):
        raise ValueError(
            "Downloaded content does not appear to be a PDF."
        )

    file_path.write_bytes(content)

    return str(file_path)