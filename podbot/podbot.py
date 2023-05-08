import feedparser
import requests
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from podreader import read_podcasts_url_from_file


class PodBot:
    def __init__(self, url: str) -> None:
        self.url = feedparser.parse(f"{url}")

    def get_podcast_properties(self):
        feed_name, author = self.url.feed.title, self.url.feed.author
        return feed_name, author

    def _format_datetime(self, date_string: str) -> str:
        return ' '.join(date_string.split()[:4])

    def get_podcast_content(self) -> list:
        podcast_content: list = []

        for content in self.url.entries:
            formatted_date = self._format_datetime(content.published)
            main_content: dict = {"date": formatted_date, "title": content.title,
                                  "duration": content.itunes_duration, 'guests': content.guests,
                                  }
            podcast_content.append(main_content)

        return podcast_content
    
    def get_download_link_to_download(self, index: int) -> str:
        return self.url.entries[index].enclosures[0].get('href')

    def download_episode(self, index: int) -> None:
        url: str = self.get_download_link_to_download(index)
        filename: Path = self._format_title_to_file(index)
        query = requests.get(url)

        with open(filename, mode='wb') as music:
            for data_chunk in query.iter_content(chunk_size=1000):
                music.write(data_chunk)

    def _format_title_to_file(self, index: int) -> Path:
        title = self.url.entries[index].title
        path = Path.home() / 'Music' / f'{title}.mp3'
        return path


url = read_podcasts_url_from_file()
user = PodBot(url[1])


f = feedparser.parse(url[0])
print(f.entries)
