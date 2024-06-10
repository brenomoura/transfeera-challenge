from typing import Optional

from pydantic import BaseModel, field_validator

PAGE = 1
PAGE_SIZE = 10


class SearchParams(BaseModel):
    page: Optional[int] = PAGE
    page_size: Optional[int] = PAGE_SIZE

    @field_validator("page")
    def validate_page(cls, value):
        if value is not None and value < 1:
            return PAGE  # just ignore and set the default value
        return value

    @field_validator("page_size")
    def validate_page_size(cls, value):
        if value is not None and value < 1:
            return PAGE_SIZE  # just ignore and set the default value
        return value
