"""Feature transformations shared by training and serving.

The bucket boundaries must stay identical in train.py and predict.py,
otherwise the model sees different inputs at inference time.
"""


def bucket_age(age: int) -> int:
    if age >= 0 and age < 32:
        return 1
    if age >= 32 and age < 38:
        return 2
    if age >= 38 and age < 47:
        return 3
    if age >= 47 and age < 60:
        return 4
    if age >= 60 and age < 90:
        return 5
    return 6


def bucket_duration(duration: int) -> int:
    if duration >= 0 and duration < 30:
        return 1
    if duration >= 30 and duration < 60:
        return 2
    if duration >= 60 and duration < 120:
        return 3
    if duration >= 120 and duration < 180:
        return 4
    if duration >= 180 and duration < 240:
        return 5
    if duration >= 240 and duration < 300:
        return 6
    if duration >= 300 and duration < 360:
        return 7
    if duration >= 360 and duration < 420:
        return 8
    if duration >= 420 and duration < 480:
        return 9
    return 10
