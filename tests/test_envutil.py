from pathlib import Path

from envutil import update_env_file


def test_update_env_file_appends_new_key(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("S3_BUCKET=example\n")

    update_env_file(env_file, "RUN_ID", "abc123")

    assert env_file.read_text().splitlines() == ["S3_BUCKET=example", "RUN_ID=abc123"]


def test_update_env_file_replaces_existing_key(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("RUN_ID=old\nS3_BUCKET=example\n")

    update_env_file(env_file, "RUN_ID", "new")

    assert env_file.read_text().splitlines() == ["RUN_ID=new", "S3_BUCKET=example"]


def test_update_env_file_creates_missing_file(tmp_path: Path) -> None:
    env_file = tmp_path / ".env.local"

    update_env_file(env_file, "DBS_ENDPOINT", "1.2.3.4")

    assert env_file.read_text() == "DBS_ENDPOINT=1.2.3.4\n"


def test_update_env_file_value_with_equals_sign(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("PASS=a\n")

    update_env_file(env_file, "PASS", "ab=cd")

    assert env_file.read_text().splitlines() == ["PASS=ab=cd"]


def test_update_env_file_key_prefix_not_confused(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("DB_NAME=one\nDB_NAME_MONI=two\n")

    update_env_file(env_file, "DB_NAME", "three")

    assert env_file.read_text().splitlines() == ["DB_NAME=three", "DB_NAME_MONI=two"]
