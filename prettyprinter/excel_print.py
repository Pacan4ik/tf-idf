import csv
from typing import List, Tuple

headers = ["File Name", "Term", "TF-IDF"]


def save_csv(data: List[Tuple[str, dict]], filename: str) -> None:
    all_rows = []
    for file_name, tfidf_dict in data:
        rows = create_tfidf_table(file_name, tfidf_dict)
        all_rows.extend(rows)

    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(all_rows)


def create_tfidf_table(doc_name: str, tfidf: dict) -> list[list[str]]:
    rows = []
    sorted_tfidf = sorted(tfidf.items(), key=lambda item: item[1], reverse=True)

    for term, value in sorted_tfidf:
        rows.append([doc_name, term, value])
    return rows
