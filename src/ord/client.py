from typing import Generator

import httpx
from bs4 import BeautifulSoup

from . import models, urls


def is_node_healthy() -> bool:
    with httpx.Client() as client:
        response = client.get(urls.is_node_healthy())
    return response.status_code == 200


def get_block_count() -> int:
    with httpx.Client() as client:
        response = client.get(urls.get_block_count())
    return int(response.content.decode("utf-8"))


def get_block(height: int) -> models.Block:
    with httpx.Client() as client:
        response = client.get(urls.get_block(height))
    return models.Block(**response.json())


def get_content(inscription_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(urls.get_content(inscription_id))
    return response.content


def get_preview(inscription_id: str) -> str:
    with httpx.Client() as client:
        response = client.get(urls.get_preview(inscription_id))
    return response.content.decode("utf-8")


def get_sat(sat: str) -> models.Sat:
    with httpx.Client() as client:
        response = client.get(urls.get_sat(sat))
    return models.Sat(**response.json())


def get_inscription(inscription_id: str) -> models.Inscription:
    with httpx.Client() as client:
        response = client.get(urls.get_inscription(inscription_id))
    return models.Inscription(**response.json())


def inscriptions(start: int = 0, stop: int | None = None) -> Generator[tuple[int, str], None, None]:
    """
    Args:
        start: inscription index to start at (inclusive)
        stop: inscription index to stop at (exclusive), or None to iterate over all inscriptions

    Returns:
        Generator yielding one inscription id at a time, starting from the
        0th inscription. Making 1 http request per 100 inscriptions.
    """
    i = start
    while True:
        with httpx.Client() as client:
            response = client.get(
                f"{urls.base()}/inscriptions/{start + 99}",
            )

        soup = BeautifulSoup(response.content, "html.parser")
        thumbnails = soup.find("div", class_="thumbnails")
        inscription_links = thumbnails.find_all("a")
        ids = [link["href"].split("/")[-1] for link in inscription_links]
        for one_id in reversed(ids):
            yield i, one_id
            i += 1
            if stop and i >= stop:
                return


def get_tx(tx_id: str) -> models.Tx:
    with httpx.Client() as client:
        response = client.get(urls.get_tx(tx_id))
    return models.Tx(**response.json())
