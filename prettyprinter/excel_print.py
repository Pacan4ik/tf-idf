import csv
from typing import List, Tuple
import pandas as pd

headers = ["File Name", "Term", "TF-IDF"]


def save_csv(data: List[Tuple[str, dict]], filename: str, threshold: float = 0) -> None:
    all_rows = concat_rows(data, threshold)

    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(all_rows)


def save_xlsx(data: List[Tuple[str, dict]], filename: str, threshold: float = 0) -> None:
    all_rows = concat_rows(data, threshold)

    df = pd.DataFrame(all_rows, columns=headers)
    df.to_excel(filename, index=False, engine='xlsxwriter')


def concat_rows(data: List[Tuple[str, dict]], threshold: float) -> List[List[str]]:
    all_rows = []
    for file_name, tfidf_dict in data:
        rows = create_tfidf_table(file_name, tfidf_dict, threshold)
        all_rows.extend(rows)
    return all_rows


def create_tfidf_table(doc_name: str, tfidf: dict, threshold: float) -> list[list[str]]:
    rows = []
    sorted_tfidf = sorted(tfidf.items(), key=lambda item: item[1], reverse=True)

    for term, value in sorted_tfidf:
        if value > threshold:
            rows.append([doc_name, term, value])
    return rows
