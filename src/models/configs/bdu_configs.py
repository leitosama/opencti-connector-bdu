from pydantic import (
    Field,
    PositiveInt,
    SecretStr,
)
from src.models.configs import ConfigBaseSettings


class _ConfigLoaderBDU(ConfigBaseSettings):
    """Interface for loading dedicated configuration."""

    # Config Loader
    base_url: str = Field(
        default="https://bdu.fstec.ru/files/documents/vulxml.zip",
        description="URL for the FSTEC BDU XML",
    )
    interval: PositiveInt = Field(
        default=6,
        description="Interval in hours to check and import new BDUs",
    )
    page_size: PositiveInt = Field(
        default=1000,
        description="Process page_size vulns at onetime"
    )