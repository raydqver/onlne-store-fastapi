from typing import Any

from fastapi_storages.integrations.sqlalchemy import ImageType as _ImageType
from fastapi_storages import FileSystemStorage


class ImageType(_ImageType):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(
            storage=FileSystemStorage(path="/tmp"), *args, **kwargs
        )
