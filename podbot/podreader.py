"""
This module handles all the podcast link save by the user
"""

import json
from pathlib import Path
from typing import List, Dict

PODCASTS_FILE = Path().home() / "my_projects/podbot/podbot/podcasts.json"


def read_podcasts_from_json() -> Dict:
    with open(PODCASTS_FILE) as file:
        reader = json.load(file)
        return reader["podcasts"]


def write_to_json(data: dict, filepath: str) -> None:
    with open(filepath, "w") as file:
        json.dump(data, file, indent=2)


def get_all_podcast_link() -> List:
    podcasts_data = read_podcasts_from_json()
    return list(podcasts_data.values())


def add_podcast_url_to_file(podcast_name: str, podcast_rss_feed: str) -> None:
    """
    Add url to the file i.e. the user subscribe to the podcast.
    :param podcast_name:
    :param podcast_rss_feed:
    :return: None
    """
    podcast_data = read_podcasts_from_json()
    podcast_data.setdefault(podcast_name, podcast_rss_feed)
    data = {"podcasts": podcast_data}
    write_to_json(data, PODCASTS_FILE)


def delete_podcast_from_file(podcast_name: str) -> None:
    podcast_data: dict = read_podcasts_from_json()
    try:
        podcast_data.pop(podcast_name)
        data = {"podcasts": podcast_data}
        write_to_json(data, PODCASTS_FILE)
    except KeyError:
        print("The feed is not in your subscription file.")
