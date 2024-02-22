import re

import fitz
from tqdm import tqdm

from data.functions import decrypting_document, get_parameters_1_part, get_parameters_2_part, get_parameters_3_part


def get_data(path: str):
    data_doc = {}
    count = 0
    data_parameters = {}
    count_2 = 0
    with tqdm((fitz.open(path)), desc='Получаем данные из файла: ') as doc:
        for page in doc:
            text = page.get_text()
            if re.search(r'[-]71\s\s5\.3\.[0-9?]{3}', text):
                if type(decrypting_document(text)) == dict:
                    count += 1
                    data_doc[count] = decrypting_document(text)
                if type(decrypting_document(text)) == list:
                    data_doc[count]['data'].extend(decrypting_document(text))
            else:
                data = re.sub(r'\s(Slot Scaling:)\s*[\\n]*([0-9A-Za-z\.\s%\/\^\-]+)\s*', r'\1 \n\2', text)
                result = data.split('-71 \n')
                if len(result) >= 2:
                    data = result[0].split('\n')
                    data_1_block = [i.strip() for i in data]
                    if len(data_1_block) > 3:
                        data_block = data_1_block[3:]
                        parameters = get_parameters_1_part(data_block)
                        if parameters is not None:
                            if isinstance(parameters, list):
                                data_parameters[count_2][parameters[0]] = parameters[1]
                            if isinstance(parameters, tuple):
                                for i in parameters:
                                    data_parameters[count_2][i[0]] = i[1]
                    for i in result[1:]:
                        count_2 += 1
                        data = i.split('\n')
                        data_2_block = [i.strip() for i in data]
                        data_parameters[count_2] = get_parameters_2_part(data_2_block)
                else:
                    for i in result:
                        data = i.split('\n')
                        data_3_block = [i.strip() for i in data]
                        parameters = get_parameters_3_part(data_3_block)
                        if parameters is not None:
                            if isinstance(parameters, list):
                                data_parameters[count_2][parameters[0]] = parameters[1]
                            if isinstance(parameters, tuple):
                                for parameter in parameters:
                                    data_parameters[count_2][parameter[0]] = i[1]

    return data_doc, data_parameters
