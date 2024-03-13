import os


def parse_sql(filename):
    """
    Lit un fichier .sql et retourne chaque instruction dans une liste de chaînes de caractères

    :param filename: le fichier .sql
    :return: liste d'instructions
    """

    current_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(current_dir, filename)

    data = open(abs_file_path, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if DELIMITER not in line:
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts


def run_sql_file(cursor, filename, accept_empty=True):
    """
    Exécute chaque instruction d'un fichier .sql

    :param cursor: un curseur pymysql.cursor ouvert
    :param filename: le fichier .sql à exécuter
    :param accept_empty: si vrai, lance une exception si le fichier est vide
    """
    sql_statements = parse_sql(filename)

    if len(sql_statements) == 0 and not accept_empty:
        raise IOError(f"File '{filename}' is empty.")

    for statement in sql_statements:
        cursor.execute(statement)
