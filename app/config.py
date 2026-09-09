from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "postgres"
    database_name: str = "crud"
    database_username: str = "postgres"
    secret_key: str = "super-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minute: int = 30

    cors_origins: str = (
        "http://localhost:3000,http://localhost:3001,http://localhost:5173,"
        "http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:3001"
    )

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_url: str | None = None

    email_host: str
    email_port: int
    email_username: str
    email_password: str

        # -----------------------------
    # Elasticsearch
    # -----------------------------

    elasticsearch_host: str = "localhost"

    elasticsearch_port: int = 9200

    elasticsearch_scheme: str = "https"

    elasticsearch_username: str = "elastic"

    elasticsearch_password: str = ""

    elasticsearch_url: str | None = None

    elasticsearch_verify_certs: bool = False

    # -----------------------------
    # Storage (uploads)
    # -----------------------------

    storage_backend: str = "disk"  # options: disk, s3, cloudinary

    # Cloudinary
    cloudinary_cloud_name: str | None = None
    cloudinary_api_key: str | None = None
    cloudinary_api_secret: str | None = None

    
    model_config = SettingsConfigDict(env_file=".env")
    

settings = Settings()