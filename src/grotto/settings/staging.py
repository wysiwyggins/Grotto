from .base import *  # noqa: F403

ALLOWED_HOSTS = ["grotto.wileywiggins.com"]


ENV = "STAGING"

# S3
DEFAULT_FILE_STORAGE = "grotto.storage.MediaStorage"
AWS_S3_ACCESS_KEY_ID = os.environ.get("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = os.environ.get("AWS_S3_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = "grotto-media"
AWS_S3_REGION = "us-east-1"
AWS_S3_MEDIA_URL = ""
