import time

import argostranslate.package
import argostranslate.translate


def creating_a_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS data_table(
        ID VARCHAR(10) NOT NULL,
        Data_length VARCHAR(20) NOT NULL,
        Length VARCHAR(20) NOT NULL,
        Name TEXT NOT NULL,
        RusName TEXT NOT NULL,
        Scaling TEXT NOT NULL,
        Range TEXT NOT NULL,
        SPN INTEGER NOT NULL
        );
        """)
    conn.commit()


def adding_data(conn, i: dict):
    with conn.cursor() as cur:
        cur.execute(""" 
        INSERT INTO data_table(ID, Data_length, Length, Name, RusName, Scaling, Range, SPN) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
        """, (i['id'], i['data_length'], i['length'], i['name'], i['rus_name'], i['scaling'], i['range'], i['spn']))
        conn.commit()


def translate_name(name: str):
    from_code = "en"
    to_code = "ru"
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
    name_rus = argostranslate.translate.translate(name, from_code, to_code)
    return name_rus


def gen(p: dict, n: dict):
    for i in range(len(p)):
        time.sleep(3)
        pgn = p[i + 1]['PGN']
        id_doc = p[i + 1]['id']
        data_length = p[i + 1]['Data_Length']
        for j in p[i + 1]['data']:
            length = j[0]
            name = j[1]
            ru_name = translate_name(name)
            paragraph = j[-1]
            for s in range(len(n)):
                m = n[s + 1]
                if len(m) == 6:
                    if m['number_paragraph'] == paragraph and m['name_paragraph'] == name and pgn == m['PGN']:
                        data = {
                            'id': id_doc,
                            'data_length': data_length,
                            'length': length,
                            'name': name,
                            'rus_name': ru_name,
                            'scaling': m['SS'],
                            'range': m['SR'],
                            'spn': m['SPN']
                        }
                        yield data
