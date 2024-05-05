from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, computed_field

from .config import get_settings


class URLBase(BaseModel):
    target_url: HttpUrl


class URL(URLBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    secret_key: Annotated[str, Field(max_length=32, min_length=32)]

    @computed_field
    def url(self) -> HttpUrl:
        base_url = get_settings().base_url
        return HttpUrl(url=f'{base_url}/{self.id}')
