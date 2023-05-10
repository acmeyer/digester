import os
import shutil
import json
import tiktoken
import requests
import mimetypes
from werkzeug.datastructures import FileStorage
from bs4 import BeautifulSoup
from db.database import supabase
from db.utils import (
    save_item_to_database, 
    save_content_to_database, 
    update_item_summary,
    get_item_by_source_url
)
from models.models import (
    Item, 
    Content, 
    Message, 
    SourceType,
)
from services.chat_completion import (
    setup_prompt,
    get_chat_completion,
)
from services.file import get_document_from_file
from services.chunks import get_text_chunks
from services.embeddings import batch_upsert_documents_for_embedding, count_tokens

GPT_4_MODEL = "gpt-4"
DEFAULT_SUMMARY_MODEL = "gpt-3.5-turbo" # "gpt-4"
OPENAI_EMBEDDING_ENCODING = "cl100k_base" # this the encoding for text-embedding-ada-002
CHUNK_TOKEN_SIZE = 200 # this is the number of tokens for text chunk
MAX_TOKENS = 500


def chunks(text, n, tokenizer):
    tokens = tokenizer.encode(text)
    """Yield successive n-sized chunks from text."""
    i = 0
    while i < len(tokens):
        # Find the nearest end of sentence within a range of 0.5 * n and 1.5 * n tokens
        j = min(i + int(1.5 * n), len(tokens))
        while j > i + int(0.5 * n):
            # Decode the tokens and check for full stop or newline
            chunk = tokenizer.decode(tokens[i:j])
            if chunk.endswith(".") or chunk.endswith("\n"):
                break
            j -= 1
        # If no end of sentence found, use n tokens as the chunk size
        if j == i + int(0.5 * n):
            j = min(i + n, len(tokens))
        yield tokens[i:j]
        i = j


def split_text(text: str) -> list[str]:
    """Split incoming text and return chunks."""
    tokenizer = tiktoken.get_encoding(OPENAI_EMBEDDING_ENCODING)
    token_chunks = list(chunks(text, CHUNK_TOKEN_SIZE, tokenizer))
    text_chunks = [tokenizer.decode(chunk) for chunk in token_chunks]
    return text_chunks


def create_new_file(filepath: str):
    file_name = filepath.split("/")[-1]
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    file_name = file_name.replace(" ", "_")
    new_file_path = f"tmp/{file_name}"
    # Copy the file to the new location
    shutil.copy(filepath, new_file_path)
    return new_file_path


def get_summary(full_text: str, model: str = DEFAULT_SUMMARY_MODEL, type: str = "short") -> str:
    prompt = setup_prompt('prompts/summarize_prompt.md')
    conversation_messages = []
    if type == "detailed":
        user_input = f"Here's the content you should summarize:\n\n{full_text}\n\n----\n\nI would like you to produce a detailed summary of this content."
    else:
        user_input = f"Here's the content you should summarize:\n\n{full_text}\n\n----\n\nI would like you to produce a short summary of this content. It should be a few sentences at most."
    conversation_messages.append(Message(role="user", text=user_input))
    return get_chat_completion(prompt, conversation_messages, model=model)


def ask_gpt_for_metadata(text: str, model: str = DEFAULT_SUMMARY_MODEL) -> dict:
    """Returns the metadata of the given text."""
    prompt = setup_prompt('prompts/metadata_prompt.md')
    conversation_messages = []
    shortened_text = split_text(text)[0]
    conversation_messages.append(Message(role="user", text=shortened_text))
    response = get_chat_completion(prompt, conversation_messages, model=model, temperature=0.5)
    return response


def get_metadata_from_file(text: str) -> dict:
    metadata = ask_gpt_for_metadata(text)
    return metadata


def read_text_from_url(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request returned an HTTP error
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None


def get_metadata_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('meta', attrs={'name': 'title'}) or soup.find('meta', attrs={'property': 'og:title'})
    description_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    author_tag = soup.find('meta', attrs={'name': 'author'}) or soup.find('meta', attrs={'property': 'og:author'})
    date_tag = soup.find('meta', attrs={'name': 'date'}) or soup.find('meta', attrs={'property': 'article:published_time'}) or soup.find('time')
    image_tag = soup.find('meta', attrs={'property': 'og:image'})

    title = title_tag['content'] if title_tag else soup.find('title').text.strip() if soup.find('title') else ''
    image = image_tag['content'] if image_tag else ''
    description = description_tag['content'] if description_tag else ''
    author = author_tag['content'] if author_tag else ''
    date_published = date_tag['content'] if date_tag and date_tag.has_attr('content') else date_tag['datetime'] if date_tag and date_tag.has_attr('datetime') else ''

    metadata = {
        'title': title,
        'image': image,
        'description': description,
        'author': author,
        'created_at': date_published
    }

    return metadata


def create_summary(
    url: str, 
    file: FileStorage = None,
    user_id: str = None,
    model: str = DEFAULT_SUMMARY_MODEL
) -> Item:
    if file:
        full_text = get_document_from_file(file)
        full_text = full_text.strip()
        num_tokens, _ = count_tokens(full_text)
        filename = file.filename.replace(" ", "_")

        # Save the file first for later reference
        temp_file_path = f"/tmp/{filename}"
        file_stream = file.read()
        mimetype, _ = mimetypes.guess_type(temp_file_path)
        with open(temp_file_path, "wb") as f:
            f.write(file_stream)
        supabase.storage.from_("files").upload(f"{user_id}/{filename}", temp_file_path, file_options={"content-type": mimetype})
        file_url = supabase.storage.from_("files").get_public_url(f"{user_id}/{filename}")
        os.remove(temp_file_path)

        metadata = get_metadata_from_file(full_text)
        metadata = json.loads(metadata)
        item = Item(
            source_url=file_url, 
            source_type=SourceType.file,
            item_metadata=metadata,
            is_processing=True
        )
        item_id = save_item_to_database(item)
        item.id = item_id
    elif url:
        item = get_item_by_source_url(url)
        if item:
            return item
        metadata = get_metadata_from_url(url)
        item = Item(
            source_url=url, 
            source_type=SourceType.url,
            item_metadata=metadata,
            is_processing=True
        )
        item_id = save_item_to_database(item)
        item.id = item_id
        full_text = read_text_from_url(url)
        full_text = full_text.strip()
        num_tokens, _ = count_tokens(full_text)

    documents_for_embedding = []
    if num_tokens > MAX_TOKENS:
        text_chunks = get_text_chunks(full_text, chunk_token_size=CHUNK_TOKEN_SIZE)
        summaries = []
        for chunk in text_chunks:
            chunk = chunk.strip()
            # Skip chunks that are too short
            if len(chunk) < 140:
                continue
            summary = get_summary(chunk, model=model, type="short")
            content = Content(
                item_id=item_id,
                text=chunk,
                summary=summary,
            )
            content_id = save_content_to_database(content)
            content.id = content_id
            summaries.append(summary)
            documents_for_embedding.append(content)
        all_summaries = "\n\n".join(summaries)
        full_response = get_summary(all_summaries, model=GPT_4_MODEL, type="detailed")
        item.summary = full_response
        update_item_summary(item_id, full_response)
        response = full_response
    else:
        response = get_summary(full_text, model=GPT_4_MODEL, type="detailed")
        content = Content(
            item_id=item_id,
            text=full_text,
            summary=response,
        )
        content_id = save_content_to_database(content)
        content.id = content_id
        documents_for_embedding.append(content)
        item.summary = response
        update_item_summary(item_id, response)

    # Save the embeddings to Pinecone
    batch_upsert_documents_for_embedding(documents_for_embedding)

    return item
