from models import database, models
from services.embeddings import count_tokens
from .database import db

def get_item_by_id(item_id: str) -> database.Item or None:
    """Gets an item from the database by id."""
    item = database.Item.query.get(item_id)
    return item

def get_item_by_source_url(source_url: str) -> database.Item or None:
    """Gets an item from the database by source."""
    item = database.Item.query.filter_by(source_url=source_url).first()
    return item

def save_item_to_database(item: models.Item):
    """Saves new feedback to the database."""
    new_item = database.Item(**item.dict())
    db.session.add(new_item)
    db.session.commit()
    item_id = new_item.id
    return item_id

def update_item_summary(item_id: str, summary: str):
    """Updates the summary of an item in the database."""
    item = database.Item.query.get(item_id)
    if item:
        item.summary = summary
        item.is_processing = False
        db.session.commit()

def save_content_to_database(content: models.Content):
    """Saves new content to the database."""
    new_content = database.Content(**content.dict())
    db.session.add(new_content)
    db.session.commit()
    content_id = new_content.id
    return content_id

def get_messages_by_user_and_item_id(user_id: str, item_id: str):
    """Gets a conversation for an item from the database by id."""
    new_messages = database.Message.query.filter_by(user_id=user_id, item_id=item_id).all()
    messages = [models.Message.from_orm(message).dict() for message in new_messages]
    return messages


def create_new_message(user_id: str, item_id: str, role: str, text: str):
    """Creates a new message in the database."""
    token_count, _ = count_tokens(text)
    message = database.Message(
        user_id=user_id, 
        item_id=item_id, 
        role=role, 
        text=text, 
        tokens_count=token_count
    )
    db.session.add(message)
    db.session.commit()
    return message


def get_items_for_user(user_id: str) -> list[database.Item]:
    """Gets all items associated with a user."""
    users_items = database.UsersItem.query.filter_by(user_id=user_id).all()
    items = [models.Item.from_orm(users_item.item).dict() for users_item in users_items]
    return items


def attach_item_to_user(user_id: str, item: models.Item):
    """Attaches an item to a user in the database."""
    if not user_id or not item.id:
        return
    users_item = database.UsersItem(user_id=user_id, item_id=item.id)
    db.session.add(users_item)
    db.session.commit()

    