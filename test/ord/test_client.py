import pytest

from src.ord import client, models


def test_is_node_healthy():
    got_health = client.is_node_healthy()
    assert got_health is True


def test_get_block_count():
    got_block_count = client.get_block_count()
    assert got_block_count >= 776261


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
    assert got_content.decode("utf-8") == want_content


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
    argnames=["start", "stop", "want_ids"],
    argvalues=[
        (
            0,
            10,
            [
                "6fb976ab49dcec017f1e201e84395983204ae1a7c2abf7ced0a85d692e442799i0",
                "26482871f33f1051f450f2da9af275794c0b5f1c61ebf35e4467fb42c2813403i0",
                "c17dd02a7f216f4b438ab1a303f518abfc4d4d01dcff8f023cf87c4403cb54cai0",
                "fb3c060cd4506731c3295311e9bc0e8d8d0d865f72c5175494c9acb31710e3dfi0",
                "c748a10a0b4d28b9a44cb0637aad24fa60ace435951fb7b83bdf43adc30c2281i0",
                "f58ad8178e7fe78624bcd814cf4b655dab8a6d5f293d4a395a8f24c49aaba78ai0",
                "22d7fa836a87e0532e9aff8d29a1b0aa872ce45545e55d9d9c73cb4309fc8bc3i0",
                "114c5c87c4d0a7facb2b4bf515a4ad385182c076a5cfcc2982bf2df103ec0fffi0",
                "d95c0fb86bc0f0dce6a732c5ab77d47e33ed24099bdb01133f768cef75a47724i0",
                "a4b5580db345db7534b74371f40562ba0d6f79fd272e05c62c05db1b62996d23i0",
            ],
        ),
        (
            10,
            50,
            [
                "7641ef7165bc59c40b269d4b2f6741ca3f34334b8c758fbba155bd0e29b4011bi0",
                "7460a1068f98e1fac798304addca4b5eed1cc9968cd5526e07c2ceb3ec7cf7b3i0",
                "517ee232143d289d70867f88cbe2b9b161ef56554bc4fa7796e672d41e2e2bf3i0",
                "16f3c32468e3e52ac20dc8fc633c686f0e31c5f34407413d12ad764ba5ad5f3bi0",
                "a6628f32a5b41b359cfe4ab038ff7c4279118ff601b9eca85eca8a64763db40ci0",
                "765cf24db22df4d7bae1cd12e5ee4780dc263486e426d8d1758eaa0515fa6fcei0",
                "f04dd50561899f650103703526a62bc2510cd1b2f185f02e76936314af42a145i0",
                "31833061114c2ee53d63dba53ef0bc2af741c87463cf573a4e211196883a5f2di0",
                "f87927419223b3c1bd9a49c065fbd1c298b9a708579eb5cb4a0a17242831500ei0",
                "9163af650dcdeeeb9a7e1f47f693b51921dce3bdf2475e69360ec83d9956f5d7i0",
                "ca009bf4cae18d22444c7a31fb05ab372816cdbfbb3fd741812dca674adf0cb5i0",
                "7acd66e6f673e82999cedd37de5a4cbe41f217ae6f1dbf26a1ddfd6ef5488051i0",
                "fd5b77f56c2b785f7266143e1dcd8b83b82050ceb7d2d7344aa3999f3cc17d4di0",
                "0c107942e4c945b6b44e193c950b0fae65d854a88b450758a3fca54017c879bei0",
                "9905c43cabe642666e43bd1c059d9093b96204330a2eeb33ac22b7142b1d57edi0",
                "562cd1136399f7a6568f41081f85c88145b87e7e70a3a53748a46902e6b84d60i0",
                "cfab194b924f7785c6e453728e1c264b89b74843633278cda3ad3f57576c1e93i0",
                "69908239157f1e069fa3a0469bad21b49187823d18e729d1ebe29b9252f5bd98i0",
                "913d65ca95afd862a71fea8d48cf95434efd3581b8d08d3f0402db526d975efai0",
                "8d9933f3c5ba17025b69fbcbf136ee237320125448e02c2eb1045286879955d5i0",
                "7b68aced40476a4caedb2a5d014974c522331291b6a78bed06bbc891cbe14c9bi0",
                "9d0ad29ef2923df9d598a1a890ead36ebbe44f1f1d77d93efa21325806311f28i0",
                "e9b1379e9a30e4e2f08fa0c38394f49aa0b92449423f966c6108be93533c17b6i0",
                "03a6381c7e224d4fe2425b5f5da3782e8bd5701e783bd0af4ee1e2700dbbb347i0",
                "b8bf03e34f8fb497941a878793f7138aab502f4a34604923cc3147ef7f6ba471i0",
                "372284d650d297f53309d790cf173d1fc5c2ee4d90250cee76c6a574ec69882fi0",
                "239882ab23041b1f017e19174f24e6397ef10a295484f395d550caaa61239b8di0",
                "7eccd70601a5a65421f560743f2661116bc88b4d73a72f4199850b498ce8e996i0",
                "5166a9ef575565ed67d63044fc442a8ef07b4ad20631442d477f784b4cb1bd29i0",
                "6b76932bb8f2478fe58d27b9f80c1c6d02ac0083ba34f9f46a2a171e9a385851i0",
                "40b3279c70d31b1c53d430a245ec012dabf173a47384f33e54db34e8e7732570i0",
                "5e1ba5c92673452e3422a553bf641cd634b46fc28fa27ecabffc917039de1869i0",
                "1aa4f606890680a9b381ba4e9130894288dd21336b82cbfd75dc19db38ece937i0",
                "adc408a32e887777007c145da9cfafda88b88917e15d06e4b0097c31cd38ab11i0",
                "b375bcce16c91f3def7871933f1696dd3681199e0f23e90d980a87dbf57e6699i0",
                "1fdbd2bbabfaa9b64bbd529d5a2d5fb1b39ffcbdd6c39601beaac5e3260c9fcei0",
                "e3e29332b269d0ae3fa28ac80427065d31b75f2c92baa729a3f8de363a0d66f6i0",
                "87d6c23065597f76aa80f588d56519a260d7a954adc4d0fdc86e9ed4eeece189i0",
                "54e47c2f0e75142d1d7a0fe585e81aceb8759b07c6cfe9fa1a0bd6c317eae8b3i0",
                "8a3e28442dec1e4c56133f75000778121bfe46ecd9fc1c447f8a8315d01017c9i0",
            ],
        ),
    ],
)
def test_inscription_ids(start: int, stop: int, want_ids: list[str]):
    generator = client.inscription_ids(start=start, stop=stop)
    got_inscriptions = list(generator)
    assert got_inscriptions == want_ids


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
