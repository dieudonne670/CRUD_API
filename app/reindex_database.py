from app.database import SessionLocal
from app.reindex import reindex_all


def main():
    """
    Rebuild every Elasticsearch index
    from PostgreSQL.
    """

    db = SessionLocal()

    try:
        reindex_all(db)

    finally:
        db.close()


if __name__ == "__main__":
    main()