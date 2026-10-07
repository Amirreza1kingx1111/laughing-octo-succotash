import os
import sqlite3
from datetime import datetime


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "instance",
    "school.db"
)

BACKUP_DIR = os.path.join(
    BASE_DIR,
    "backups"
)

MAX_BACKUPS = 10


def get_backup_files():
    if not os.path.isdir(BACKUP_DIR):
        return []

    files = []

    for filename in os.listdir(BACKUP_DIR):

        if not (
            filename.startswith("school_")
            and filename.endswith(".db")
        ):
            continue

        path = os.path.join(
            BACKUP_DIR,
            filename
        )

        if os.path.isfile(path):
            files.append(path)

    files.sort(
        key=os.path.getmtime,
        reverse=True
    )

    return files


def verify_database(path):
    connection = sqlite3.connect(path)

    try:
        result = connection.execute(
            "PRAGMA integrity_check;"
        ).fetchone()

        if not result or result[0] != "ok":
            raise RuntimeError(
                f"Backup integrity check failed: {result}"
            )

    finally:
        connection.close()


def create_backup():

    if not os.path.isfile(DB_PATH):
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    os.makedirs(
        BACKUP_DIR,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    backup_name = (
        f"school_{timestamp}.db"
    )

    backup_path = os.path.join(
        BACKUP_DIR,
        backup_name
    )

    source = sqlite3.connect(
        DB_PATH
    )

    destination = sqlite3.connect(
        backup_path
    )

    try:
        source.backup(destination)

    finally:
        destination.close()
        source.close()

    verify_database(backup_path)

    cleanup_old_backups()

    return backup_path


def cleanup_old_backups():

    backups = get_backup_files()

    for old_backup in backups[MAX_BACKUPS:]:

        try:
            os.remove(old_backup)

        except OSError:
            pass


if __name__ == "__main__":

    path = create_backup()

    print("BACKUP OK")
    print(f"Created: {path}")
    print("Integrity: ok")
