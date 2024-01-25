"""
PodBot: This interacts with any rss feed pass into it.
"""
from pathlib import Path
from typing import Final, List, Tuple

import feedparser
import requests
from rich.console import Console
from rich.progress import Progress

BYTE_TO_WRITE_PER_NSECONDS: Final = 1024
BYTE_CONVERSION_VALUE: Final = 1048576


def _format_datetime(date_string: str) -> str:
    return " ".join(date_string.split()[:4])


class PodBot:
    """
    PodBot: The podbot class that does every function included in it.
    """

    def __init__(self, podcast_url: str) -> None:
        self.url = feedparser.parse(f"{podcast_url}")
        self.console = Console()

    def get_podcast_properties(self) -> dict:
        """
        This get the properties of podcast url passed into it.
        :return: dict
        """
        podcast_metadata = {
            "feed": self.url.feed.get("title", "None"),
            "author": self.url.feed.get("author", "None"),
        }
        return podcast_metadata

    @property
    def get_podcast_content(self) -> List[dict]:
        """
        This get all episode in a podcast feed.
        :return: List[dict]
        """
        podcast_content: list = []

        for content in self.url.entries:
            formatted_date = _format_datetime(content.published)
            main_content: dict = {
                "date": formatted_date,
                "title": content.title,
                "duration": content.itunes_duration,
                "guests": content.get("authors", "None"),
            }
            podcast_content.append(main_content)

        return podcast_content, self.url.feed.get("title", "None")

    def get_download_link_to_download(self, index: int) -> str:
        """
        This extracts the download link of an episode.
        :param index: int
        :return: str
        """
        episode_url = self.url.entries[index].enclosures[0].get("href")
        return episode_url

    def download_episode(self, index: int) -> None:
        """
        This download an episode which is retrieves through the index of an episode.
        :param index: int
        :return: None
        """
        episode_link_to_download: str = self.get_download_link_to_download(index)
        title = self._format_title_to_file(index)
        filename = self._save_path(episode_link_to_download)
        query = requests.get(episode_link_to_download, stream=True)
        music_length = int(query.headers.get("content-length", 0))
        mebibyte_length = music_length / BYTE_CONVERSION_VALUE
        downloading_length = 0

        with Progress() as progress:
            task = progress.add_task(f"{title}\n", total=music_length)

            with open(filename, mode="wb") as music:
                for data_chunk in query.iter_content(
                    chunk_size=BYTE_TO_WRITE_PER_NSECONDS
                ):
                    downloading_length += (
                        BYTE_TO_WRITE_PER_NSECONDS / BYTE_CONVERSION_VALUE
                    )
                    progress.update(
                        task,
                        advance=BYTE_TO_WRITE_PER_NSECONDS,
                        description=f"{title}"
                        f" \n{downloading_length:.2f}/{mebibyte_length:.2f}MB",
                    )
                    music.write(data_chunk)

    def _format_title_to_file(self, index: int) -> Tuple[Path, str]:
        """
        This handles where the file will be saved to and clear format name
        :param index: int
        :return: Tuple[Path, str]
        """
        title = self.url.entries[index].title
        return title

    def _save_path(self, download_link: str) -> Path:
        import re

        url = download_link
        pattern = r"/(\d+-[\w-]+\.mp3)$"

        match = re.search(pattern, url)

        if match:
            result = match.group(1)

        path = Path.home() / "Music" / f"{result}"
        return path
