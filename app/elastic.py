from elasticsearch import Elasticsearch

from app.config import settings


# -------------------------------------------------
# Elasticsearch URL
# -------------------------------------------------

ELASTICSEARCH_URL = (
    settings.elasticsearch_url
    or f"{settings.elasticsearch_scheme}://{settings.elasticsearch_host}:{settings.elasticsearch_port}"
)


# -------------------------------------------------
# Elasticsearch Client
# -------------------------------------------------

es = Elasticsearch(
    ELASTICSEARCH_URL,

    basic_auth=(
        settings.elasticsearch_username,
        settings.elasticsearch_password,
    ),

    verify_certs=settings.elasticsearch_verify_certs,
)


# -------------------------------------------------
# Check Connection
# -------------------------------------------------

def check_elasticsearch() -> bool:
    """
    Returns True if Elasticsearch is reachable.
    """

    return es.ping()


# -------------------------------------------------
# Create Index
# -------------------------------------------------

def create_index(
    index_name: str,
    mapping: dict,
):

    """
    Creates an index if it doesn't exist.
    """

    if not es.indices.exists(index=index_name):

        es.indices.create(
            index=index_name,
            mappings=mapping,
        )


# -------------------------------------------------
# Delete Index
# -------------------------------------------------

def delete_index(index_name: str):

    """
    Deletes an index.
    """

    if es.indices.exists(index=index_name):

        es.indices.delete(index=index_name)


# -------------------------------------------------
# Index Document
# -------------------------------------------------

def index_document(
    index: str,
    document_id: int,
    document: dict,
):

    """
    Inserts a document.
    """

    es.index(
        index=index,
        id=document_id,
        document=document,
    )


# -------------------------------------------------
# Update Document
# -------------------------------------------------

def update_document(
    index: str,
    document_id: int,
    document: dict,
):

    """
    Updates an existing document.
    """

    es.update(
        index=index,
        id=document_id,
        doc=document,
    )


# -------------------------------------------------
# Delete Document
# -------------------------------------------------

def delete_document(
    index: str,
    document_id: int,
):

    """
    Deletes one document.
    """

    try:

        es.delete(
            index=index,
            id=document_id,
        )

    except Exception:
        pass


# -------------------------------------------------
# Search
# -------------------------------------------------

def search(
    index: str,
    query: dict,
    size: int = 20,
):

    """
    Executes a search query.
    """

    return es.search(
        index=index,
        query=query,
        size=size,
    )