import requests
from bs4 import BeautifulSoup
import re
import urllib


def is_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


visited_sites = []


def crawler(url, depth):
    try:
        if not is_url(url):
            return

        base_url = urllib.parse.urlparse(url).hostname

        if base_url in visited_sites:
            return

        visited_sites.append(base_url)

        print(f"{depth} => {base_url}")
        r = requests.get(url)
        text = r.text
        html = BeautifulSoup(text, 'html.parser')
        anchor_tags = html.find_all('a')
        urls = [a.get('href') for a in anchor_tags]

        for nested_url in urls:
            crawler(nested_url, depth + 1)
    except:
        return


crawler("https://realpython.com/python-requests/", 1)
