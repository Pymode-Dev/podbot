from argparse import ArgumentParser

from main import show_podcasts_table, show_episodes_table, download_episodes


def parse_args():
    parser = ArgumentParser(
        description="Manage your podcast feed in the command line.",
        add_help=True,
        prog="PodBot",
        epilog="Thanks for using PodBot",
    )

    subparser = parser.add_subparsers(help="Command", dest="command")

    show_podcast = subparser.add_parser(
        "sp", help="Show all available podcast in the json file."
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

    return parser.parse_args()


def main():
    args = parse_args()

    match args.command:
        case "sp":
            show_podcasts_table()
        case "se":
            podcast = args.podcast_name
            show_episodes_table(podcast)
        case "d":
            podcast_name = args.podcast_name
            download_episodes(podcast_name, args.episode)


main()
