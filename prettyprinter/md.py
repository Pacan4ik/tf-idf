from typing import List, Tuple
from tabulate import tabulate

headers = ["File Name", "Term", "TF-IDF"]


def print_table(data: List[Tuple[str, dict]], threshold: float = 0.001, limit: int = -1) -> None:
    all_rows = []
    for file_name, tfidf_dict in data:
        rows = create_tfidf_table(file_name, tfidf_dict, threshold, limit)
        all_rows.extend(rows)

    table = tabulate(all_rows, headers, tablefmt="github")
    print(table)


def create_tfidf_table(doc_name: str, tfidf: dict, threshold: float, limit: int) -> list[list[str]]:
    rows = []
    sorted_tfidf = sorted(tfidf.items(), key=lambda item: item[1], reverse=True)

    if limit > 0:
        sorted_tfidf = sorted_tfidf[:limit]

    first_row = True
    for term, value in sorted_tfidf:
        if value > threshold:
            if first_row:
                rows.append([doc_name, term, f"{value:.3f}"])
                first_row = False
            else:
                rows.append(["", term, f"{value:.3f}"])

    return rows
