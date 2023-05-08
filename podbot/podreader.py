import functools


@functools.cache
def read_podcasts_url_from_file() -> list:
    with open("podcasts_url.txt", mode='r', newline='') as file:
        reader = [line.strip('\n') for line in file]

    return reader

@functools.cache
def add_podcast_url_to_file(podcast_name: str) -> None:
    with open("podcasts_url.txt", mode='a', newline='\n') as file:
        file.write(podcast_name)

