from pathlib import Path

from apps.users.services.firestore_service import FirestoreUserService

TESTS_DIR = Path(__file__).parent
TEST_LOGGER_NAME = "test"
IMAGE_PATH = TESTS_DIR / "files" / "miku.jpg"
LARGE_AVATAR = TESTS_DIR / "files" / "large_avatar.png"

firestore_service = FirestoreUserService()
