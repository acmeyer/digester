from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from db.database import db
import uuid

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String, nullable=False, unique=True)
    photo_url = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summary = db.Column(db.String)
    source_url = db.Column(db.String, unique=True)
    source_type = db.Column(db.Enum('file', 'url', name='source_type_enum'), nullable=False)
    item_metadata = db.Column(JSONB)
    is_processing = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = db.Column(UUID(as_uuid=True), db.ForeignKey('items.id'), nullable=False)
    text = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    content_metadata = db.Column(JSONB)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    item = relationship("Item")

class UsersItem(db.Model):
    __tablename__ = 'users_items'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(UUID(as_uuid=True), db.ForeignKey('items.id'), nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User")
    item = relationship("Item")

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(UUID(as_uuid=True), db.ForeignKey('items.id'), nullable=False)
    role = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    tokens_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User")
    item = relationship("Item")

