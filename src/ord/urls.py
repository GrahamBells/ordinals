"""URL config and formatters"""

import functools
import os

import pydantic


class UrlConfig(pydantic.BaseModel):
    is_testnet = os.getenv("USE_TEST_NETWORK", "false") in {"true", "1"}

    @property
    def is_mainnet(self) -> bool:
        return not self.is_testnet


@functools.lru_cache()
def get_url_config() -> UrlConfig:
    return UrlConfig()


def base() -> str:
    return "https://ordinals.com" if get_url_config().is_mainnet else "https://testnet.ordinals.com"


def is_node_healthy() -> str:
    return f"{base()}/status"


def get_block_count() -> str:
    return f"{base()}/block-count"


def get_block(height: int) -> str:
    return f"https://ordapi.xyz/block/{height}"


def get_content(inscription_id: str) -> str:
    return f"{base()}/content/{inscription_id}"


def get_preview(inscription_id: str) -> str:
    return f"{base()}/preview/{inscription_id}"


def get_sat(sat: str) -> str:
    return f"https://ordapi.xyz/sat/{sat}"


def get_inscription(inscription_id: str) -> str:
    return f"https://ordapi.xyz/inscription/{inscription_id}"


def get_tx(tx_id: str) -> str:
    return f"https://ordapi.xyz/tx/{tx_id}"
