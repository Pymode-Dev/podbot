"""
This module combine the user interface and the backend stuff together
"""

from typing import List

from .podbot_ui import EpisodesTable, PodcastsTable
from .podreader import (
    get_all_podcast_link,
    read_podcasts_from_json,
    delete_podcast_from_file,
    add_podcast_url_to_file,
)

from .podbot import PodBot


class DisplayPodcast:
    def get_all_podcasts_content(self) -> List[dict]:
        podcasts_data: List = []
        links: List = get_all_podcast_link()

        for index, link in enumerate(links):
            podbot = PodBot(link)
            podcasts_data.append(podbot.get_podcast_properties())
        return podcasts_data

    def show_podcasts_table(self):
        podcasts_feed: List[dict] = self.get_all_podcasts_content()
        podcast_user_interface = PodcastsTable(podcasts_feed)
        podcast_user_interface.display_podcasts()

    def execute(self):
        self.show_podcasts_table()


class DisplayEpisode:
    def __init__(self, name: str) -> None:
        self.name = name

    def get_podcast_episodes(self, podcast_name: str) -> List[dict]:
        link = read_podcasts_from_json()[podcast_name]
        if link:
            podcast = PodBot(link)
            podcast_episodes = podcast.get_podcast_content
            return podcast_episodes

    def show_episodes_table(self, podcast_name: str):
        episodes, podcast = self.get_podcast_episodes(podcast_name)
        episode_table = EpisodesTable(episodes, podcast)
        episode_table.display_episodes()

    def execute(self) -> str:
        self.show_episodes_table(self.name)


class DownloadEpisode:
    def __init__(self, name: str, index: int) -> None:
        self.name = name
        self.index = index

    def download_episodes(self, podcast_name: str, episode_index: List[int]) -> None:
        link = read_podcasts_from_json()[podcast_name]
        podcast = PodBot(link)
        for i in episode_index:
            podcast.download_episode(i)

    def execute(self) -> str:
        self.download_episodes(self.name, self.index)
        return "Download Successfully"


class DeleteFeed:
    def __init__(self, podcast_name: str) -> None:
        self.name = podcast_name

    def execute(self):
        delete_podcast_from_file(self.name)
        return f"{self.name} deleted successfully"


class AddFeed:
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    def execute(self) -> str:
        add_podcast_url_to_file(self.name, self.url)
        return f"{self.name} has been added"
