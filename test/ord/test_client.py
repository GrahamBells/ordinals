import pytest

from src.ord import client, models


@pytest.mark.parametrize(
    argnames=["height", "want_hash", "want_size"],
    argvalues=[
        (1, "00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048", 215),
        (2, "000000006a625f06636b8bb6ac7b960a8d03705d1ace08b1a19da3fdcc99ddbd", 215),
        (3, "0000000082b5015589a3fdf2d4baff403e6f0be035a5d9742c1cae6295464449", 215),
        (4, "000000004ebadb55ee9096c9a2f8880e09da59c0d68b1c228da88e48844a1485", 215),
        (5, "000000009b7262315dbf071787ad3656097b892abffd1f95a1a022f896f533fc", 215),
    ],
)
def test_get_block(height: int, want_hash: str, want_size: int):
    got_block = client.get_block(height)
    assert got_block.hash == want_hash
    assert got_block.size == want_size


@pytest.mark.parametrize(
    argnames=["inscription", "want_content"],
    argvalues=[
        (
            "3d91f7983bbb9ef05f05a874bb78d79fa15d2e38fddb9f2f866bcbb853b9460di0",
            """emo.eth wuz here xoxo\n0x22eed066b155cacff80c4ae52c723c000999786c5b2b99d616dd99c21ca45a006d961f2053a70adcfebfd8ec3cf83b3e3759c65efde03ac94802799a8d12c1ec01""",
        ),
        (
            "0e75686a1a78f79de4263b2d6344a2884630696c64f9202776b6f2e9db5b5ceei0",
            """i am sat 1283640386681191
of degree 0°93456′1056″386681191‴
and percentile 61.125732766342665%

my true name is 'etifttseiww'
and my rarity is common

i was born may 31st, 2014

~
""",
        ),
    ],
)
def test_get_content(inscription: str, want_content: str):
    got_content = client.get_content(inscription)
    assert got_content == want_content


@pytest.mark.parametrize(
    argnames=["inscription", "want_preview"],
    argvalues=[
        (
            "f255329ff815546c99edd672ab545afa96e3b3a570b0d202f60ff6b7c7e71ba7i0",
            """<!doctype html>
<html lang=en>
  <head>
    <meta charset=utf-8>
    <meta name=format-detection content='telephone=no'>
    <link href=/static/preview-text.css rel=stylesheet>
    <script src=/static/preview-text.js defer></script>
  </head>
  <body>
    <pre>1283640386667641
</pre>
    <noscript>
      <pre>1283640386667641
</pre>
    </noscript>
  </body>
</html>
""",
        ),
    ],
)
def test_get_preview(inscription: str, want_preview):
    got_preview = client.get_preview(inscription)
    assert got_preview == want_preview


@pytest.mark.parametrize(
    argnames=["sat_id", "want_sat"],
    argvalues=[
        (
            "1283640386667641",
            models.Sat(
                block="/block/303456",
                cycle=0,
                decimal="303456.386667641",
                degree="0°93456′1056″386667641‴",
                epoch=1,
                inscription="/inscription/f255329ff815546c99edd672ab545afa96e3b3a570b0d202f60ff6b7c7e71ba7i0",
                name="etifttsfcya",
                offset=386667641,
                percentile="61.12573276569743%",
                period=150,
                rarity="common",
                timestamp="2014-05-31 10:31:34 UTC",
            ),
        )
    ],
)
def test_get_sat(sat_id: str, want_sat: models.Sat):
    got_sat = client.get_sat(sat_id)
    assert got_sat == want_sat


@pytest.mark.parametrize(
    argnames=["inscription_id", "want_inscription"],
    argvalues=[
        (
            "ff4503ab9048d6d0ff4e23def81b614d5270d341ce993992e93902ceb0d4ed79i0",
            models.Inscription(
                id="ff4503ab9048d6d0ff4e23def81b614d5270d341ce993992e93902ceb0d4ed79i0",
                title="Inscription 42149",
                address="bc1p3rfd76c37af87e23g4z6tts0zu52u6frjh92m9uq5evxy0sr7hvslly59y",
                content="/content/ff4503ab9048d6d0ff4e23def81b614d5270d341ce993992e93902ceb0d4ed79i0",
                content_length="85700 bytes",
                content_type="image/webp",
                genesis_fee=151788,
                genesis_height="/block/775796",
                genesis_transaction="/tx/ff4503ab9048d6d0ff4e23def81b614d5270d341ce993992e93902ceb0d4ed79",
                inscription_number=42149,
                location="ff4503ab9048d6d0ff4e23def81b614d5270d341ce993992e93902ceb0d4ed79:0:0",
                offset="0",
                output="/output/ff4503ab9048d6d0ff4e23def81b614d5270d341ce993992e93902ceb0d4ed79:0",
                output_value=10000,
                preview="/preview/ff4503ab9048d6d0ff4e23def81b614d5270d341ce993992e93902ceb0d4ed79i0",
                sat="/sat/1914287520444193",
                timestamp="2023-02-09 22:54:59 UTC",
            ),
        )
    ],
)
def test_get_inscription(inscription_id: str, want_inscription: models.Inscription):
    got_inscription = client.get_inscription(inscription_id)
    assert got_inscription == want_inscription


@pytest.mark.parametrize(
    argnames=["tx_id", "want_tx"],
    argvalues=[
        (
            "ff4503ab9048d6d0ff4e23def81b614d5270d341ce993992e93902ceb0d4ed79",
            models.Tx(
                address="bc1p3rfd76c37af87e23g4z6tts0zu52u6frjh92m9uq5evxy0sr7hvslly59y",
                script_pubkey="OP_PUSHNUM_1 OP_PUSHBYTES_32 88d2df6b11f7527f65514545a5ae0f1728ae692395caad9780a658623e03f5d9",
                value=10000,
            ),
        )
    ],
)
def test_get_tx(tx_id: str, want_tx: models.Tx):
    got_tx = client.get_tx(tx_id)
    assert got_tx == want_tx
