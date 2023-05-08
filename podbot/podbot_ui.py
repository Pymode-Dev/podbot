from rich.table import Table
from rich.console import Console


class PodcastsTable:
    def __init__(self, index: str, feed: str, author: str, data: list):
        self.index = index
        self.feed = feed
        self.author = author
        self.data = data
        self.console = Console()
        self.table = Table()

    def display_podcasts(self):
        self.table.add_column(self.index)
        self.table.add_column(self.feed)
        self.table.add_column(self.author)
        
        for i, data in enumerate(self.data, start=1):
            feed = data.get('feed', 'None')
            author = data.get('author', 'None')
            self.table.add_row(str(i), feed, author)

        self.console.print(self.table)


data = [{'feed': 'Talk Python', 'author': 'Micheal Kennedy'},
        {'feed': 'Dev Journey', 'author': 'Tim Bourgnion'},
        {'feed': 'Pybites', 'author': 'Julian and Bob'},
        {'feed': 'Python Bites'}]
user = PodcastsTable('Index', 'Feed', 'Author', data)
user.display_podcasts()
