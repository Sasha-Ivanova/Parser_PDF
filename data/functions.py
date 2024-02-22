import configparser
import re


def get_data_config():
    config = configparser.ConfigParser()
    config.read('setting.ini', encoding='UTF-8')
    database = config.get('db', 'database')
    user = config.get('db', 'user')
    password = config.get('db', "password")
    path = config.get('file', 'path')
    name_file = config.get('file', 'name_file')
    return path, name_file, database, user, password


def get_parameters_1_block(i: list):
    ind = i.index('Data Length:')
    dl_data = i[ind+1]
    ind_pgn = i.index('Parameter Group')
    pgn_data = i[ind_pgn+1]
    id_data = i[ind_pgn + 2]
    paragraph = []
    pd_index = i.index('paragraph')
    list_data = i[pd_index+2:]
    ld = []
    for i in list_data:
        if len(ld) < 5:
            ld.append(i)
        else:
            del ld[-1]
            paragraph.append(ld)
            ld = []
    parameters = {
        'Data_Length': dl_data,
        'PGN': pgn_data,
        'id': id_data,
        'data': paragraph
        }
    return parameters


def decrypting_document(text: str):
    repl_text = re.sub(r'(\()\s*(\w+)*\s*(\))', r'\2', text)
    repl_text_2 = re.sub(r'SPN\s{2}and\s(paragraph)\sApproved', r'\1', repl_text)
    data = repl_text_2.split('–71')
    result = data[1].split('-71 \n5.3.')
    if len(result) == 3:
        docs = [i.split(' \n') for i in result[1:]]
        for doc in docs:
            docs_new = [i.strip() for i in doc]
            return get_parameters_1_block(docs_new)
    if len(result) == 2:
        docs = [i.split(' \n') for i in result]
        if len(docs[0]) == 2:
            docs_new = docs[1]
            return get_parameters_1_block(docs_new)
        else:
            parameters_dop = []
            parameters = docs[0][3:]
            if len(parameters) > 1 and parameters[0] != '':
                dop_list = []
                for parameter in parameters:
                    dop_list.append(parameter)
                    if len(dop_list) > 5:
                        parameters_dop.append(dop_list[0:-2])
                        dop_list = []
            return parameters_dop


def get_parameters_2_part(data: list):
    global pgn_p
    if 'Parameter Group Name and Acronym Doc. and Paragraph' in data:
        pgn_ind = data.index('Parameter Group Name and Acronym Doc. and Paragraph')
        if len(data[pgn_ind:]) >= 3:
            pgn_p = data[pgn_ind + 2]
        sr_ind = data.index('Slot Range:')
        sr = data[sr_ind + 1]
        ss_ind = data.index('Slot Scaling:')
        ss = data[ss_ind + 1]
        spn_ind = data.index('SPN:')
        spn = data[spn_ind + 1]
        parameters = {
            'PGN': pgn_p,
            'SR': sr,
            'SS': ss,
            'SPN': spn,
            'number_paragraph': data[0],
            'name_paragraph': data[1]
        }
        return parameters
    else:
        if 'SPN:' in data:
            spn_ind = data.index('SPN:')
            spn = data[spn_ind + 1]
            sr_ind = data.index('Slot Range:')
            sr = data[sr_ind + 1]
            ss_ind = data.index('Slot Scaling:')
            ss = data[ss_ind + 1]
            parameters = {
                'SR': sr,
                'SS': ss,
                'SPN': spn,
                'number_paragraph': data[0],
                'name_paragraph': data[1]
            }
            return parameters
        else:
            if 'Slot Range:' in data:
                sr_ind = data.index('Slot Range:')
                sr = data[sr_ind + 1]
                ss_ind = data.index('Slot Scaling:')
                ss = data[ss_ind + 1]
                parameters = {
                    'SR': sr,
                    'SS': ss,
                    'number_paragraph': data[0],
                    'name_paragraph': data[1]
                }
                return parameters
            else:
                if 'Slot Scaling:' in data:
                    ss_ind = data.index('Slot Scaling:')
                    ss = data[ss_ind + 1]
                    parameters = {
                        'SS': ss,
                        'number_paragraph': data[0],
                        'name_paragraph': data[1]
                    }
                    return parameters
                else:
                    parameters = {
                        'number_paragraph': data[0],
                        'name_paragraph': data[1]
                    }
                    return parameters


def get_parameters_1_part(data: list):
    global pgn_p
    if 'Parameter Group Name and Acronym Doc. and Paragraph' in data:
        pgn_ind = data.index('Parameter Group Name and Acronym Doc. and Paragraph')
        if len(data[pgn_ind:]) >= 3:
            pgn_p = data[pgn_ind + 2]

            if 'Slot Scaling:' in data:
                sr_ind = data.index('Slot Range:')
                sr = data[sr_ind + 1]
                ss_ind = data.index('Slot Scaling:')
                ss = data[ss_ind + 1]
                spn_ind = data.index('SPN:')
                spn = data[spn_ind + 1]
                return ['PGN', pgn_p], ['SR', sr], ['SS', ss], ['SPN', spn]
            else:
                if 'Slot Range:' in data:
                    sr_ind = data.index('Slot Range:')
                    sr = data[sr_ind + 1]
                    spn_ind = data.index('SPN:')
                    spn = data[spn_ind + 1]
                    return ['SR', sr], ['SPN', spn], ['PGN', pgn_p]
                else:
                    if 'SPN:' in data:
                        spn_ind = data.index('SPN:')
                        spn = data[spn_ind + 1]
                        return ['SPN', spn], ['PGN', pgn_p]
                    else:
                        return ['PGN', pgn_p]
    else:
        if 'SPN:' in data:
            spn_ind = data.index('SPN:')
            spn = data[spn_ind + 1]
            if 'Slot Range:' in data:
                sr_ind = data.index('Slot Range:')
                sr = data[sr_ind + 1]
                if 'Slot Scaling:' in data:
                    ss_ind = data.index('Slot Scaling:')
                    ss = data[ss_ind + 1]
                    return ['SR', sr], ['SS', ss], ['SPN', spn]
        else:
            if 'Slot Range:' in data:
                sr_ind = data.index('Slot Range:')
                sr = data[sr_ind + 1]
                if 'Slot Scaling:' in data:
                    ss_ind = data.index('Slot Scaling:')
                    ss = data[ss_ind + 1]
                    return ['SR', sr], ['SS', ss]
            else:
                if 'Slot Scaling:' in data:
                    ss_ind = data.index('Slot Scaling:')
                    ss = data[ss_ind + 1]
                    return ['SS', ss]
                else:
                    if len(data) > 1:
                        if data[0] == '' and data[1].isdigit():
                            return ['PGN', data[1]]


def get_parameters_3_part(data: list):
    global pgn_p
    if 'Parameter Group Name and Acronym Doc. and Paragraph' in data:
        pgn_ind = data.index('Parameter Group Name and Acronym Doc. and Paragraph')
        if len(data[pgn_ind:]) >= 3:
            pgn_p = data[pgn_ind + 2]

            if 'Slot Scaling:' in data:
                sr_ind = data.index('Slot Range:')
                sr = data[sr_ind + 1]
                ss_ind = data.index('Slot Scaling:')
                ss = data[ss_ind + 1]
                spn_ind = data.index('SPN:')
                spn = data[spn_ind + 1]
                return ['SR', sr], ['SS', ss], ['SPN', spn], ['PGN', pgn_p]
            else:
                if 'Slot Range:' in data:
                    sr_ind = data.index('Slot Range:')
                    sr = data[sr_ind + 1]
                    spn_ind = data.index('SPN:')
                    spn = data[spn_ind + 1]
                    return ['SR', sr], ['SPN', spn], ['PGN', pgn_p]
                else:
                    if 'SPN:' in data:
                        spn_ind = data.index('SPN:')
                        spn = data[spn_ind + 1]
                        return ['SPN', spn], ['PGN', pgn_p]
    else:
        if 'SPN:' in data:
            spn_ind = data.index('SPN:')
            spn = data[spn_ind + 1]
            if 'Slot Range:' in data:
                sr_ind = data.index('Slot Range:')
                sr = data[sr_ind + 1]
                if 'Slot Scaling:' in data:
                    ss_ind = data.index('Slot Scaling:')
                    ss = data[ss_ind + 1]
                    return ['SR', sr], ['SS', ss], ['SPN', spn]
        else:
            if 'Slot Range:' in data:
                sr_ind = data.index('Slot Range:')
                sr = data[sr_ind + 1]
                if 'Slot Scaling:' in data:
                    ss_ind = data.index('Slot Scaling:')
                    ss = data[ss_ind + 1]
                    return ['SR', sr], ['SS', ss]
            else:
                if 'Slot Scaling:' in data:
                    ss_ind = data.index('Slot Scaling:')
                    ss = data[ss_ind + 1]
                    return ['SS', ss]
