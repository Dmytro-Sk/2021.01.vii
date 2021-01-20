from urllib.request import Request, urlopen
import re
import json


def get_json_from_response_body(**kwargs):
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    r = Request(f'{url}', headers={'User-Agent': USER_AGENT})
    raw_data = urlopen(r).read().decode('utf-8')
    data = json.loads(re.search(pattern, raw_data).group(2))

    with open(f'../{project_name}_jquery.json', 'w') as f:
        json.dump(data, f, indent=2)


url = 'https://www.hemnet.se/bostader?item_types%5B%5D=bostadsratt&keywords=balkong'
pattern = r'("itemListElement": )(\[.*\])'
project_name = re.search(r'(www\.)([\w.]+)(/)', url).group(2).replace('.', '_')

get_json_from_response_body(url=url, pattern=pattern, project_name=project_name)
