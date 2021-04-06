import utility as u
import requests
from bs4 import BeautifulSoup


def get_lecture_titles(content):
    return [t.text for t in content.find_all('h3')]

def psalm_with_breaks(psalm):
    """Adds line breaks so the psalm is readable."""
    lines = psalm.splitlines()
    result = ''
    first_line = True
    lines_size = len(lines)
    for i in range(lines_size):
        result += lines[i]
        if i + 1 < lines_size:
            result += '\n'
            if lines[i + 1].startswith('R. '):
                result += '\n'
            if lines[i].startswith('R. '):
                result += '\n'
    return result


def strip_empty_lines(text):
    return '\n'.join([t for t in text.splitlines() if t])

def main():
    r = requests.get("https://bible.usccb.org/daily-bible-reading")
    if r.status_code == 200:
        result = BeautifulSoup(r.content, 'html.parser')
        readings = result.find_all('div', class_="content-body")
        lecture_titles = get_lecture_titles(result)
        texts = []
        for t, r in zip(lecture_titles, readings):
            texts.append(t)
            if 'psalm' in t.lower() or 'alleluia' in t.lower():
                for br_tag in r.find_all('br'):
                    br_tag.replace_with('\n')
                texts.append(psalm_with_breaks(strip_empty_lines(r.text.strip())))
            else:
                if r.find('p') is None:
                    for br_tag in r.find_all('br'):
                        br_tag.replace_with('\n')
                texts.append(r.text.strip())
        print(texts)


if __name__ == "__main__":
    main()