import arxiv


def search_arxiv(
    query: str,
    max_results: int = 10,
) -> list[dict]:

    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=(
            arxiv.SortCriterion.Relevance
        ),
    )

    print(query)    

    papers = []

    for result in client.results( search ):
        paper = {
            "title": result.title,
            "authors": [
                author.name
                for author in result.authors
            ],
            "abstract": result.summary,
            "published": (
                result.published.isoformat()
            ),
            "url": result.entry_id,
            "pdf_url": result.pdf_url,
        }
        print(paper)
        papers.append(paper)
        

    return papers