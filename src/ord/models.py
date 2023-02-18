import pydantic


class BaseModel(pydantic.BaseModel):
    class Config:
        # Necessary since aliases have spaces in them
        allow_population_by_field_name = True


class Block(BaseModel):
    hash: str
    previous_block_hash: str = pydantic.Field(..., alias="previous blockhash")
    size: int
    target: str
    timestamp: str
    weight: int


class Sat(BaseModel):
    block: str
    cycle: int
    decimal: str
    degree: str
    epoch: int
    inscription: str
    name: str
    offset: int
    percentile: str
    period: int
    rarity: str
    timestamp: str


class Inscription(BaseModel):
    id: str
    address: str
    content: str
    content_length: str = pydantic.Field(..., alias="content length")
    content_type: str = pydantic.Field(..., alias="content type")
    genesis_fee: int = pydantic.Field(..., alias="genesis fee")
    genesis_height: int = pydantic.Field(..., alias="genesis height")
    genesis_transaction: str = pydantic.Field(..., alias="genesis transaction")
    inscription_number: int  # = pydantic.Field(..., alias="inscription_number")
    location: str
    offset: str
    output: str
    output_value: int = pydantic.Field(..., alias="output value")
    preview: str
    sat: str
    timestamp: str
    title: str

    @pydantic.validator("genesis_height", pre=True)
    def sanitize_genesis_height(cls, v) -> int:
        match v:
            case int():
                return v
            case str():
                return int(v.split("/")[-1])
            case _:
                raise ValueError("Must be either a string or int")

    @pydantic.validator("genesis_transaction", pre=True)
    def sanitize_genesis_transaction(cls, v) -> str:
        return v.split("/")[-1]


class Tx(BaseModel):
    address: str
    value: int
    script_pubkey: str = pydantic.Field(..., alias="script pubkey")
