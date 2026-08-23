import pytest

from features import bucket_age, bucket_duration


def _legacy_age(age: int) -> int:
    """The inline transform as it appeared in the original train.py/predict.py."""
    return (
        1
        if age >= 0 and age < 32
        else 2
        if age >= 32 and age < 38
        else 3
        if age >= 38 and age < 47
        else 4
        if age >= 47 and age < 60
        else 5
        if age >= 60 and age < 90
        else 6
    )


def _legacy_duration(duration: int) -> int:
    """The inline transform as it appeared in the original train.py/predict.py."""
    return (
        1
        if duration >= 0 and duration < 30
        else 2
        if duration >= 30 and duration < 60
        else 3
        if duration >= 60 and duration < 120
        else 4
        if duration >= 120 and duration < 180
        else 5
        if duration >= 180 and duration < 240
        else 6
        if duration >= 240 and duration < 300
        else 7
        if duration >= 300 and duration < 360
        else 8
        if duration >= 360 and duration < 420
        else 9
        if duration >= 420 and duration < 480
        else 10
    )


@pytest.mark.parametrize(
    ("age", "expected"),
    [
        (25, 1),
        (31, 1),  # last value of bucket 1
        (32, 2),  # bucket 2 starts
        (37, 2),
        (38, 3),
        (46, 3),
        (47, 4),
        (59, 4),
        (60, 5),
        (89, 5),
        (90, 6),
        (120, 6),
    ],
)
def test_bucket_age_boundaries(age: int, expected: int) -> None:
    assert bucket_age(age) == expected


@pytest.mark.parametrize(
    ("duration", "expected"),
    [
        (0, 1),
        (29, 1),  # last raw value of bucket 1
        (30, 2),
        (59, 2),
        (60, 3),
        (119, 3),
        (120, 4),
        (239, 5),
        (240, 6),
        (299, 6),
        (300, 7),
        (359, 7),
        (360, 8),
        (419, 8),
        (420, 9),
        (479, 9),
        (480, 10),
        (1000, 10),
    ],
)
def test_bucket_duration_boundaries(duration: int, expected: int) -> None:
    assert bucket_duration(duration) == expected


def test_bucket_age_matches_legacy_transform() -> None:
    assert all(bucket_age(a) == _legacy_age(a) for a in range(-10, 120))


def test_bucket_duration_matches_legacy_transform() -> None:
    assert all(bucket_duration(d) == _legacy_duration(d) for d in range(-10, 600))
