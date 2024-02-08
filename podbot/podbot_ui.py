"""
This handles the user interface in the terminal.
Author: Pymode-dev
"""

from dataclasses import dataclass
from rich.console import Console
from rich.table import Table


@dataclass
class PodcastsTable:
    """
    Class that handles UI of all podcast url the user save, if user want to
    display all podcast present.
    """

    def __init__(self, podcasts_data: list):
        self.data = podcasts_data
        self.console = Console(soft_wrap=True)
        self.table = Table(
            style="blue",
            caption="All Podcasts",
            show_lines=True,
            title="Podcasts",
            caption_justify="left",
            title_justify="left",
        )

    def display_podcasts(self) -> None:
        """
        This display the table if the expected data is passed into it
        :return: None
        """
        self.table.add_column("Index")
        self.table.add_column("Feed")
        self.table.add_column("Author")

        for i, channels in enumerate(self.data, start=1):
            index = str(i)
            feed = channels.get("feed", "None")
            author = channels.get("author", "None")
            self.table.add_row(index, feed, author)

        self.console.print(self.table)


class EpisodesTable:
    """
    This class the UI of episodes in a podcast channel.
    """

    def __init__(
        self,
        data: list,
        podcast: str,
    ):
        self.data = data
        self.console = Console(soft_wrap=True)
        self.table = Table(
            style="blue",
            caption="All Episodes",
            show_lines=True,
            title=f"{podcast.upper()}",
            caption_justify="left",
            title_justify="center",
            title_style="blue",
        )

    def display_episodes(self) -> None:
        """
        This display the episodes if the expected data is passed into it.
        :return: None
        """
        self.table.add_column("Index")
        self.table.add_column("Title")

        for i, episode in enumerate(self.data, start=0):
            index = i
            title = episode.get("title", "None").title()
            has_guest = episode.get("guests", "None")
            if has_guest != "None":
                has_guest = has_guest[0].get("name", "None")
            date = episode.get("date", "None")
            duration = episode.get("duration", "None")
            self.table.add_row(f"#{index}", date, title, has_guest, duration)

        self.console.print(self.table)
