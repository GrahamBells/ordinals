[![pypi](https://img.shields.io/pypi/v/ordeal.svg)](https://pypi.python.org/pypi/ordeal)

A sandbox for working with [ord](https://github.com/casey/ord): `pip install ordeal`

For now, api calls go through https://ordapi.xyz/ but an [official api is in the works](https://github.com/casey/ord/pull/1662). Will switch to that once available, or start wrapping the ord crate from python.

## Setup

Clone, `poetry install` then `pre-commit install`.

`poetry run pytest`


## Usage

All subject to change. Just exploring the api for now.

A simple example of iterating through inscriptions and printing any with plaintext content:

```python
from ord import client

for i, inscription_id in client.inscriptions(start=0, stop=100):
    inscription = client.get_content(inscription_id)
    try:
        plaintext = inscription.decode("utf-8")
        print(i, inscription_id, "plaintext content")
        print(plaintext, "\n\n")
    except UnicodeDecodeError:
        pass
```
