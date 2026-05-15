from pathlib import Path

from apps.users.services.firestore_service import FirestoreUserService
from config.settings.base import ENV_FILE

assert ENV_FILE == '.env.test', "Environment must be .env.test!"

TESTS_DIR = Path(__file__).parent
TEST_LOGGER_NAME = "test"
IMAGE_PATH = TESTS_DIR / "files" / "miku.jpg"
LARGE_AVATAR = TESTS_DIR / "files" / "large_avatar.png"
LARGE_PHOTO = TESTS_DIR / "files" / "large_photo.jpg"

firestore_service = FirestoreUserService()
