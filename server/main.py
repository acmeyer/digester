import os
import sys
import logging

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError, Unauthorized
from flask_cors import CORS

from services.summarize import (
    create_summary,
)
from services.embeddings import query_embeddings
from services.chat_completion import get_chat_completion, setup_prompt
from db.database import db
from db.utils import (
    get_item_by_id,
    get_messages_by_user_and_item_id,
    create_new_message,
    attach_item_to_user,
    get_items_for_user
)
from models.models import (
    Item,
    Message,
    MessageRole
)
from dotenv import load_dotenv
load_dotenv('.env')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

PORT = 8080
DATABASE_URL = os.environ.get("DATABASE_URL")
assert DATABASE_URL, "DATABASE_URL not set"
 # HEADS UP! this is for local use only, typically would want to get this from a user session
ADMIN_USER_ID = os.environ.get("ADMIN_USER_ID")
assert ADMIN_USER_ID, "ADMIN_USER_ID not set"

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/summarize', methods=['POST'])
def summarize():
    file = request.files.get('file')
    url = request.form.get('url')
    if not file and not url:
        raise BadRequest(description="No file or URL provided")

    user_id = ADMIN_USER_ID
    response = create_summary(url=url, file=file, user_id=user_id)
    # Attach item to user if it doesn't already exist
    attach_item_to_user(user_id, response)
    return jsonify({
        "item": response.dict()
    }), 200      

@app.route('/summaries', methods=['GET'])
def get_summaries():
    user_id = ADMIN_USER_ID
    items = get_items_for_user(user_id)
    return jsonify({
        "items": items
    }), 200


@app.route('/summaries/<item_id>', methods=['GET'])
def get_item_summary(item_id):
    item = get_item_by_id(item_id)

    if not item:
        raise NotFound(description="Item not found")

    return jsonify({
        "item": Item.from_orm(item).dict()
    }), 200


@app.route('/summaries/<item_id>/messages', methods=['GET'])
def get_conversation(item_id):
    user_id = ADMIN_USER_ID
    item = get_item_by_id(item_id)
    conversation_messages = get_messages_by_user_and_item_id(user_id, item_id)

    if len(conversation_messages) == 0:
        # If conversation is empty, create an initial message with the summary
        summary_message=f"**Summary:** {item.summary}"
        create_new_message(user_id=user_id, item_id=item_id, role="assistant", text=summary_message)
        # Refresh conversation messages
        conversation_messages = get_messages_by_user_and_item_id(user_id, item_id)

    return jsonify({
        "messages": conversation_messages
    }), 200


@app.route('/summaries/<item_id>/messages', methods=['POST'])
def new_message(item_id):
    user_id = ADMIN_USER_ID
    request_data = request.get_json()
    message = request_data.get('message')
    create_new_message(user_id=user_id, item_id=item_id, role="user", text=message)
    
    relevant_docs = query_embeddings(query=message, item_id=item_id, top_k=3)
    relevant_content = "\n\n".join([f"{doc.get('metadata').get('text')}" for doc in relevant_docs])
    user_content = f"""
    Relevant content:
    {relevant_content}
    =====
    Question:
    {message}
    """
    user_message = Message(role=MessageRole.user, text=user_content)
    conversation_messages = get_messages_by_user_and_item_id(user_id, item_id)
    conversation_messages = [Message(role=m.get('role'), text=m.get('text')) for m in conversation_messages]
    conversation_messages.append(user_message)
    prompt = setup_prompt('prompts/chat_prompt.md')
    answer = get_chat_completion(prompt, messages=conversation_messages)
    create_new_message(user_id=user_id, item_id=item_id, role="assistant", text=answer)
    conversation_messages = get_messages_by_user_and_item_id(user_id, item_id)

    return jsonify({
        "messages": conversation_messages
    }), 200


@app.errorhandler(Unauthorized)
def handle_unauthorized(e: Unauthorized):
    return jsonify({'error': str(e.description)}), 401


@app.errorhandler(NotFound)
def handle_not_found(e: NotFound):
    return jsonify({'error': str(e.description)}), 404


@app.errorhandler(BadRequest)
def handle_bad_request(e: BadRequest):
    return jsonify({'error': str(e.description)}), 400


@app.errorhandler(InternalServerError)
def handle_internal_server_error(e: InternalServerError):
    return jsonify({'error': str(e.description)}), 500


def start():
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
