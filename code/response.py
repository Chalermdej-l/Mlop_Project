"""Shape prediction results into the /predict API response."""

from __future__ import annotations

import datetime


def prepare_response(predictions: list, data: list, version: str) -> dict:
    results = [(str(data[i]["id"]), int(o)) for i, o in enumerate(predictions)]
    return {
        "model_version": version,
        "date": datetime.datetime.today().strftime("%Y-%m-%d"),
        "result": results,
    }
