import os

from argparse import ArgumentParser
from collections import OrderedDict

import command


def parse_args():
    parser = ArgumentParser(
        description="Manage your podcast feed in the command line.",
        add_help=True,
        prog="PodBot",
        epilog="Thanks for using PodBot",
    )

    subparser = parser.add_subparsers(help="Command", dest="command")

    show_podcast = subparser.add_parser(
        "sp", help="Show all available podcast you add."
    )

    show_episode = subparser.add_parser(
        "se", help="Show all episode in a podcast channel."
    )
    show_episode.add_argument("podcast_name", type=str)

    download_episode = subparser.add_parser("d", help="Download an episode or episodes")
    download_episode.add_argument(
        "podcast_name", help="The name of the podcast in your feed"
    )
    download_episode.add_argument(
        "episode", help="episode to download in number", type=int, nargs="+"
    )

    add_podcast = subparser.add_parser("add", help="Add podcast feed to file")
    add_podcast.add_argument(
        "podcast_name", help="The name of the podcast serves as the key", type=str
    )
    add_podcast.add_argument(
        "podcast_url", help="The url of the podcast feed", type=str
    )

    delete_podcast = subparser.add_parser(
        "delete", help="Delete podcast fee[Unsubscribe]"
    )
    delete_podcast.add_argument(
        "podcast_name",
        help="The podcast name will be used to remove the url feed",
        type=str,
    )

    return parser.parse_args()


class Options:
    """
    Command Pattern Logic.
    """

    def __init__(self, command) -> None:
        self.command = command

    def choose(self) -> None:
        self.command.execute()


def get_podcast_name(parser) -> str:
    return parser.podcast_name if "podcast_name" in parser else None


def get_episode(parser) -> str:
    return parser.episode if "episode" in parser else None


def get_url(parser) -> str:
    return parser.podcast_url if "podcast_url" in parser else None


def clear_screen() -> None:
    clear = "clear" if os.name == "posix" else "cls"
    os.system(clear)


def main():
    args = parse_args()
    podcast_name = get_podcast_name(args)
    episode = get_episode(args)
    url_feed = get_url(args)

    options = OrderedDict(
        {
            "sp": Options(command.DisplayPodcast()),
            "se": Options(command.DisplayEpisode(podcast_name)),
            "d": Options(command.DownloadEpisode(podcast_name, episode)),
            "delete": Options(command.DeleteFeed(podcast_name)),
            "add": Options(command.AddFeed(podcast_name, url_feed)),
        }
    )
    clear_screen()
    options[args.command].choose()


if __name__ == "__main__":
    main()
