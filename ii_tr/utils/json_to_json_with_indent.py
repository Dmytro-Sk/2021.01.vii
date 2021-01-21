import json


def json_wit_indent(file_name):
    with open(f'../{file_name}.json') as f:
        data = json.load(f)
    with open(f'../{file_name}.json', 'w') as n_f:
        json.dump(data, n_f, indent=2)


json_wit_indent(file_name='json_reviews_1')
