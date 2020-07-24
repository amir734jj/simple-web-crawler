from bs4 import BeautifulSoup
import re, urllib, requests, sys
import asyncio

# List of visited sites
visited_sites = []

def is_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'                                                                 # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'                                                                         # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'                                                # ...or ip
        r'(?::\d+)?'                                                                          # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None


async def crawler(url, depth, max_depth):
  # If max depth reached
  if depth >= max_depth:
    return

  try:
      # If url is not valid
      if not is_url(url):
          return

      # Resolve the base url
      base_url = urllib.parse.urlparse(url).hostname

      # If base url is already visited
      if base_url in visited_sites:
          return

      visited_sites.append(base_url)

      print(f"{depth} => {base_url}")
      r = requests.get(url)
      text = r.text
      html = BeautifulSoup(text, 'html.parser')
      anchor_tags = html.find_all('a')
      urls = [a.get('href') for a in anchor_tags]

      await asyncio.wait([crawler(nested_url, depth + 1, max_depth) for nested_url in urls])
  except:
      return


url = sys.argv[1]                       # url
max_depth = int(sys.argv[2])            # max depth

asyncio.run(crawler(url, 1, max_depth)) # start crawler