import argparse as ap
import os


def parse_arguments():
    parser = ap.ArgumentParser(description='Выделяет частоту термина для массива файлов.')
    parser.add_argument('--source', type=str, required=True,
                        help='Путь к директории с данными.')
    parser.add_argument('--out_format', type=str, default='console', choices=['console', 'csv', 'xlsx'],
                        help='Формат вывода: console, csv, xlsx.')
    parser.add_argument('--output', type=str,
                        help='Путь для сохранения результатов (обязательно для форматов csv и xlsx).')
    parser.add_argument('--threshold', type=float, default=0.005,
                        help='Пороговое значение для фильтрации TF-IDF значений.')
    parser.add_argument('--limit', type=int, default=15,
                        help='Количество выводимых терминов')
    parser.add_argument('--stop_words', type=str,
                        help='Путь для пользовательских стоп-слов')

    arguments = parser.parse_args()
    if arguments.out_format in ['csv', 'xlsx'] and not arguments.output:
        parser.error("--output обязателен при выборе форматов вывода csv или xlsx.")
    if arguments.stop_words:
        valid_path(arguments.stop_words)
        os.environ['STOPWORDS_PATH'] = arguments.stop_words
    return arguments


def valid_path(path):
    if not os.path.exists(path):
        raise ap.ArgumentTypeError(f"Путь '{path}' не существует.")
    return path


if __name__ == '__main__':
    args = parse_arguments()
    valid_path(args.source)

    from preprocessing import preproccessing
    from tfidfstat import tfidf
    from prettyprinter import md
    from prettyprinter import excel_print

    docs = preproccessing.text_extraction(args.source)
    try:
        res = tfidf.tfidf(docs)
    except UserWarning as e:
        print('Директория --source должна содержать минимум 2 файла форматов pdf или word.')
        raise SystemExit(e)

    file_name_stat = [(article.file_name, tfidf_dict) for article, tfidf_dict in res]

    if args.out_format == 'console':
        md.print_table(file_name_stat, threshold=args.threshold, limit=args.limit)
    if args.out_format == 'csv':
        excel_print.save_csv(file_name_stat, args.output, threshold=args.threshold, limit=args.limit)
    if args.out_format == 'xlsx':
        excel_print.save_xlsx(file_name_stat, args.output, threshold=args.threshold, limit=args.limit)
