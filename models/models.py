from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime
from uuid import UUID
import json

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super(UUIDEncoder, self).default(obj)
    

class UuidBaseModel(BaseModel):
    class Config:
        json_encoders = {
            UUID: str,
        }


class SummaryType(str, Enum):
    short = "short"
    long = "long"
    detailed = "detailed"


class SourceType(str, Enum):
    file = "file"
    url = "url"


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(UuidBaseModel):
    role: MessageRole
    text: str

    class Config:
        orm_mode = True


class ItemMessage(UuidBaseModel):
    id: Optional[UUID] = None
    item_id: UUID
    role: MessageRole
    text: str
    created_at: datetime

    class Config:
        orm_mode = True


class ItemMetadata(UuidBaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None


class Item(UuidBaseModel):
    id: Optional[UUID] = None
    source_url: str
    source_type: SourceType
    is_processing: Optional[bool] = False
    summary: Optional[str] = None
    item_metadata: Optional[ItemMetadata] = None

    class Config:
        orm_mode = True


class ContentMetadata(UuidBaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None


class Content(UuidBaseModel):
    id: Optional[UUID] = None
    text: str
    item_id: UUID
    summary: str
    content_metadata: Optional[ContentMetadata] = None

    class Config:
        orm_mode = True


class ContentWithEmbedding(Content):
    embedding: Optional[list[float]] = None


class DocumentMetadata(UuidBaseModel):
    source_type: Optional[SourceType] = None
    source_id: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None
    author: Optional[str] = None


class DocumentChunkMetadata(DocumentMetadata):
    document_id: Optional[str] = None


class DocumentChunk(UuidBaseModel):
    id: Optional[str] = None
    text: str
    metadata: DocumentChunkMetadata
    embedding: Optional[list[float]] = None


class DocumentChunkWithScore(DocumentChunk):
    score: float


class Document(UuidBaseModel):
    id: Optional[str] = None
    text: str
    metadata: Optional[DocumentMetadata] = None


class DocumentWithChunks(Document):
    chunks: list[DocumentChunk]


class DocumentMetadataFilter(UuidBaseModel):
    document_id: Optional[str] = None
    source_type: Optional[SourceType] = None
    source_id: Optional[str] = None
    author: Optional[str] = None
    start_date: Optional[str] = None  # any date string format
    end_date: Optional[str] = None  # any date string format


class Query(UuidBaseModel):
    query: str
    filter: Optional[DocumentMetadataFilter] = None
    top_k: Optional[int] = 3


class QueryWithEmbedding(Query):
    embedding: list[float]


class QueryResult(UuidBaseModel):
    query: str
    results: list[DocumentChunkWithScore]