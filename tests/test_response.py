import datetime
import re

from response import prepare_response


def test_prepare_response_shape() -> None:
    data = [{"id": 1}, {"id": 2}, {"id": 3}]
    result = prepare_response([0, 1, 0], data, "abc123")

    assert result["model_version"] == "abc123"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", result["date"])
    assert result["date"] == datetime.date.today().isoformat()


def test_prepare_response_pairs_ids_with_predictions() -> None:
    data = [{"id": 10}, {"id": 20}]
    result = prepare_response([1, 0], data, "v1")

    assert result["result"] == [("10", 1), ("20", 0)]


def test_prepare_response_casts_types() -> None:
    data = [{"id": 7}]
    result = prepare_response([1.0], data, "v1")

    pair = result["result"][0]
    assert isinstance(pair[0], str)
    assert isinstance(pair[1], int)
