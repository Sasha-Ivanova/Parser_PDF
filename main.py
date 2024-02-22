import psycopg2

from data.data import get_data
from data.functions import get_data_config
from db.db import db_data

def main():
    configuration = get_data_config()
    full_path = f'{configuration[0]}\{configuration[1]}'
    data = get_data(full_path)
    data_doc = data[0]
    data_parameters = data[1]
    conn = psycopg2.connect(
        database=configuration[2],
        user=configuration[3],
        password=configuration[4]
    )
    db_data(conn, data_doc, data_parameters)


if __name__ == '__main__':
    main()
