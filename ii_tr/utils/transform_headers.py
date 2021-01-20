import json


def transform_headers(file_name):
    with open(f'../{file_name}.txt') as f:
        lines = f.readlines()
        keys = (line.rstrip().replace(' ', '').split(':')[0] for line in lines)
        values = (line.rstrip().replace(' ', '').split(':')[1] for line in lines)
        headers_dict = dict(zip(keys, values))

    with open(f'../{file_name}.txt', 'w') as n_f:
        n_f.write('headers = ')
        json.dump(headers_dict, n_f, indent=2)


transform_headers(file_name='headers')
