from urllib.request import Request, urlopen


def robots_txt(domain, project_name):
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    r = Request(f'https://www.{domain}/robots.txt', headers={'User-Agent': USER_AGENT})
    data = urlopen(r).read()

    with open(f'../{project_name}_robots.txt', 'w', encoding='utf-8') as f:
        f.write(data.decode('utf-8'))


domain = 'sephora.com'
robots_txt(domain=domain, project_name=domain.replace('.', '_'))
