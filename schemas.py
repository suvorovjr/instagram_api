from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


class CursorModel(BaseModel):
    before: str
    after: str


class PagingModel(BaseModel):
    cursors: CursorModel
    next: Optional[str] = Field(default=None)


class PagesDataModel(BaseModel):
    access_token: str
    category: str
    name: str
    id: str


class PagesResponseModel(BaseModel):
    data: List[PagesDataModel]
    paging: PagingModel


class InstBusinessModel(BaseModel):
    id: str


class InstagramIDResponseModel(BaseModel):
    instagram_business_account: InstBusinessModel
    id: str


class MediaModel(BaseModel):
    id: str
    permalink: str
    timestamp: datetime
    comments_count: int


class MediaResponseModel(PagesResponseModel):
    data: List[MediaModel]
