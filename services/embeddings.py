import os
import openai
import pinecone
import tiktoken
from tenacity import retry, wait_random_exponential, stop_after_attempt
from dotenv import load_dotenv
load_dotenv()

from models.models import ContentWithEmbedding, Content

# Read environment variables for Pinecone configuration
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT", "us-east1-gcp")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX")
assert PINECONE_API_KEY is not None
assert PINECONE_ENVIRONMENT is not None
assert PINECONE_INDEX is not None

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

EMBEDDINGS_MODEL = "text-embedding-ada-002"
OPENAI_EMBEDDING_ENCODING = "cl100k_base" # this the encoding for text-embedding-ada-002
MAX_EMBEDDING_TOKENS = 8191 # the maximum for text-embedding-ada-002 is 8191
UPSERT_BATCH_SIZE = 100 # Pinecone suggested batch size for upserts
INDEX_DIMENSION = 1536 # dimensionality of OpenAI ada v2 embeddings

def count_tokens(text: str) -> int:
    """Returns the number of tokens in the given text."""
    encoding = tiktoken.get_encoding(OPENAI_EMBEDDING_ENCODING)
    tokens = encoding.encode(text)
    num_tokens = len(tokens)
    return num_tokens, tokens

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str, model=EMBEDDINGS_MODEL) -> list[float]:
    text = text.replace("\n", " ") # OpenAI says removing newlines leads to better performance
    return openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def get_embeddings(texts: list[str]) -> list[list[float]]:
    # Call the OpenAI API to get the embeddings
    response = openai.Embedding.create(input=texts, model=EMBEDDINGS_MODEL)

    # Extract the embedding data from the response
    data = response["data"]  # type: ignore

    # Return the embeddings as a list of lists of floats
    return [result["embedding"] for result in data]


def batch_upsert_documents_for_embedding(documents: list[Content]):
    # Get embeddings for documents
    documents_text = [doc.text for doc in documents]
    embeddings = get_embeddings(documents_text)
    documents_with_embeddings = []
    # Update the document objects with the embeddings
    for i, doc in enumerate(documents):
        # Assign the embedding from the embeddings list to the chunk object
        documents_with_embeddings.append(
            ContentWithEmbedding(
                **doc.dict(),
                embedding=embeddings[i]
            )
        )

    vectors = []
    # Loop through the docs
    for doc in documents_with_embeddings:
        print(f"Upserting document_id: {doc.id}")
        # Create a vector tuple of (id, embedding, metadata)
        # Add the text and document id to the metadata dict
        pinecone_metadata = {}
        pinecone_metadata["text"] = doc.text
        pinecone_metadata["summary"] = doc.summary
        pinecone_metadata["item_id"] = str(doc.item_id)
        vector = (str(doc.id), doc.embedding, pinecone_metadata)
        vectors.append(vector)

    # Split the vectors list into batches of the specified size
    batches = [
        vectors[i : i + UPSERT_BATCH_SIZE]
        for i in range(0, len(vectors), UPSERT_BATCH_SIZE)
    ]
    # Upsert each batch to Pinecone
    index = get_pinecone_index()
    for batch in batches:
        try:
            print(f"Upserting batch of size {len(batch)}")
            index.upsert(vectors=batch)
            print(f"Upserted batch successfully")
        except Exception as e:
            print(f"Error upserting batch: {e}")
            raise e


# Using Pinecone for embeddings search
def get_pinecone_index():
    # Pick a name for the new index
    index_name = PINECONE_INDEX

    # Creates new index
    indexes = pinecone.list_indexes()
    fields_to_index = ["item_id"]
    if index_name not in indexes:
        print(f'Index not found, creating index: {index_name}')
        pinecone.create_index(
            index_name,
            dimension=INDEX_DIMENSION,
            metadata_config={"indexed": fields_to_index},
        )

    print(f'Using index: {index_name}')
    index = pinecone.Index(index_name=index_name)
    return index

def query_embeddings(query: str, item_id: str, top_k: int = 3):
    """Queries embeddings using the content in the specified namespace and returns results."""
    index_name = PINECONE_INDEX
    index = pinecone.Index(index_name=index_name)
    # Create vector embeddings based on the query
    embedded_query = get_embedding(query)
    query_result = index.query(
        vector=embedded_query, 
        include_metadata=True,
        top_k=top_k,
        filter={"item_id": item_id}
    )
    
    matches = query_result.matches
    return matches