from tqdm import tqdm

from db.functions import creating_a_table, adding_data, gen


def db_data(conn, p: dict, k: dict):
    creating_a_table(conn)
    for i in tqdm((gen(p, k)), desc='Добавляем данные в БД: '):
        adding_data(conn, i)
