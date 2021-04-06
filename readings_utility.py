import requests
from collections import OrderedDict
from bs4 import BeautifulSoup


class ReadingsParser:

    english_url = "https://bible.usccb.org/daily-bible-reading"
    spanish_url = "https://bible.usccb.org/es/bible/lecturas"

    def get_reading_title(self, content):
        return [t.text for t in content.find_all('h2')]

    def get_lecture_titles(self, content):
        return [t.text for t in content.find_all('h3')]

    def psalm_with_breaks(self, psalm):
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

    def get_verse(self, content):
        return [t.text.strip() for t in content.find_all('div', class_='address')]

    def strip_empty_lines(self, text):
        return '\n'.join([t for t in text.splitlines() if t])

    def get_web_url(self, language):
        if language == 'en':
            return self.english_url
        else:
            return self.spanish_url

    def get_web_source(self, url):
        # Retrieve the page source
        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return r.content

    def soupify(self, source):
        """Simply calls beatiful Soup with the html."""
        soup = BeautifulSoup(source, 'html.parser')
        return soup

    def parse_source(self, source):
        readings_data = list()
        readings_data.append(self.get_reading_title(source)[3].strip())
        lecture_titles = self.get_lecture_titles(source)
        verses = self.get_verse(source)

        readings = source.find_all('div', class_="content-body")
        texts = []
        for t, v, r, in zip(lecture_titles, verses, readings):
            reading_section = OrderedDict()
            reading_section['reading_type'] = t
            reading_section['reading_verse'] = v
            if 'psalm' in t.lower() or 'alleluia' in t.lower():
                for br_tag in r.find_all('br'):
                    br_tag.replace_with('\n')
                texts.append(self.psalm_with_breaks(self.strip_empty_lines(r.text.strip())))
            else:
                if r.find('p') is None:
                    for br_tag in r.find_all('br'):
                        br_tag.replace_with('\n')
                texts.append(r.text.strip())
            reading_section['reading_content'] = texts
            readings_data.append(reading_section)
        return readings_data

    def get_readings(self, language='en'):
        url = self.get_web_url(language)
        source = self.get_web_source(url=url)
        soup = self.soupify(source)
        readings = self.parse_source(soup)
        return readings
