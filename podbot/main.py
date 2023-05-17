"""
This module combine the user interface and the backend stuff together
"""

from typing import List

from podbot_ui import EpisodesTable, PodcastsTable
from podreader import get_all_podcast_link, read_podcasts_from_json

from podbot import PodBot


def get_all_podcasts_content() -> List[dict]:
    podcasts_data: List = []
    links: List = get_all_podcast_link()

    for index, link in enumerate(links):
        podbot = PodBot(link)
        podcasts_data.append(podbot.get_podcast_properties())
    return podcasts_data


def show_podcasts_table():
    podcasts_feed: List[dict] = get_all_podcasts_content()
    podcast_user_interface = PodcastsTable("Index", "Feed", "Author", podcasts_feed)
    podcast_user_interface.display_podcasts()


def get_podcast_episodes(podcast_name: str) -> List[dict]:
    podcast_data = read_podcasts_from_json()
    link: str = podcast_data.get(podcast_name, "None")
    if link:
        podcast = PodBot(link)
        podcast_episodes = podcast.get_podcast_content()
        return podcast_episodes


def show_episodes_table(podcast_name: str):
    episodes, podcast = get_podcast_episodes(podcast_name)
    episode_table = EpisodesTable(
        "Index", "Date", "Title", "Guest", "Duration", episodes, podcast
    )
    episode_table.display_episodes()


def download_episodes(podcast_name: str, episode_index: List[int]) -> None:
    podcast_data = read_podcasts_from_json()
    link: str = podcast_data.get(podcast_name)
    podcast = PodBot(link)
    for i in episode_index:
        podcast.download_episode(i)
