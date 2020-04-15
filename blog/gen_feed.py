from bs4 import BeautifulSoup

rss = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
  <title>Andrew Carr Data Science with Esoteric Programming Languages</title>
  <link>https://andrewnc.github.io/blog/blog.html</link>
  <description>Exploring data science problems but only using esoteric programming languages.</description>
"""

soup = BeautifulSoup(open("blog.html"), "html.parser")
for val in soup.find_all("article"):

    title_element = val.find_all("a")[0]
    title = title_element.text
    title_url = title_element['href']
    time = val.find_all("time")[0].text
    description = val.find_all("section")[0].text


    rss += "<item>\n"
    rss += f"<title>{title}</title>\n"
    rss += f"<link>{title_url}</link>\n"
    rss += f"<description>{description}</description>\n"
    rss += f"<pubDate>{time}</pubDate>\n"
    rss += "</item>\n"


rss += "</channel>\n"
rss += "</rss>"

with open("feed.xml", "w") as f:
    f.write(rss)