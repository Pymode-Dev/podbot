import functools
import requests

from configparser import ConfigParser
from typing import Dict

UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"


@functools.cache
def read_assembly_api_info() -> Dict:
    parser = ConfigParser()
    parser.read("secrets.ini")
    return parser["assembly_api"]


api_info = read_assembly_api_info()
headers = {"authorization": api_info["api_key"], "content-type": "application.json"}


def _read_remote_file(file_url: str):
    response = requests.get(file_url, headers=headers)
    return response.status


print(_read_remote_file())
