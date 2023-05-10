import os
import pinecone
from dotenv import load_dotenv
load_dotenv('.env')

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT", "us-central1-gcp")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX")
assert PINECONE_API_KEY is not None
assert PINECONE_ENVIRONMENT is not None
assert PINECONE_INDEX is not None

INDEX_DIMENSION = 1536

def create_pinecone_index(index_name: str):
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

if __name__ == '__main__':
  pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
  create_pinecone_index(PINECONE_INDEX)